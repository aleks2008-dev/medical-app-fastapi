from uuid import UUID
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.domain.entities.user import User, UserRole
from app.repository.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, create_reset_token, verify_reset_token, verify_refresh_token, revoke_token
from app.core.token_storage import token_storage
from app.core.email import send_reset_email

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        if user.disabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is disabled"
            )
        return user

    async def create_tokens(self, user: User) -> dict:
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = await create_refresh_token(data={"sub": str(user.id)})
        
        # Сохраняем данные сессии
        session_data = {
            "user_id": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "login_time": datetime.now(timezone.utc).isoformat()
        }
        await token_storage.store_user_session(str(user.id), session_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def register_user(self, name: str, surname: str, email: str, password: str, phone: str = None) -> User:
        # Проверяем, существует ли пользователь
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Создаем нового пользователя
        hashed_password = get_password_hash(password)
        user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
            phone=phone,
            role=UserRole.user
        )
        
        await self.user_repository.add(user)
        return user

    async def refresh_access_token(self, refresh_token: str) -> dict:
        from app.core.security import verify_token
        try:
            user_id = await verify_token(refresh_token)
            
            # Проверяем, что refresh токен сохранен в Redis
            if not await verify_refresh_token(refresh_token, user_id):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            user = await self.user_repository.get(id=UUID(user_id))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            # Отзываем старый refresh токен
            await token_storage.revoke_refresh_token(user_id)
            
            # Создаем новые токены
            return await self.create_tokens(user)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

    async def request_password_reset(self, email: str):
        user = await self.user_repository.get_by_email(email)
        if not user:
            # Не раскрываем информацию о том, существует ли пользователь
            return {"message": "If user exists, reset email will be sent"}
        
        reset_token = create_reset_token(email)
        
        # Сохраняем токен в базе данных
        await self.user_repository.update(
            str(user.id), 
            reset_token=reset_token,
            reset_token_expires=datetime.now(timezone.utc) + timedelta(hours=1)
        )
        
        # Отправляем email
        await send_reset_email(email, reset_token)
        return {"message": "If user exists, reset email will be sent"}

    async def reset_password(self, token: str, new_password: str):
        email = verify_reset_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        user = await self.user_repository.get_by_email(email)
        if not user or user.reset_token != token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Проверяем срок действия токена
        if user.reset_token_expires and user.reset_token_expires < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired"
            )
        
        # Обновляем пароль и очищаем токен
        hashed_password = get_password_hash(new_password)
        await self.user_repository.update(
            str(user.id),
            hashed_password=hashed_password,
            reset_token=None,
            reset_token_expires=None
        )
        
        return {"message": "Password successfully reset"}
    
    async def logout_user(self, user_id: str, access_token: str) -> dict:
        """Выход пользователя"""
        # Отзываем access токен
        await revoke_token(access_token)
        
        # Отзываем сессию и refresh токен
        await token_storage.revoke_user_session(user_id)
        
        return {"message": "Successfully logged out"}