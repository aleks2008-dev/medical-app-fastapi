from uuid import UUID
from typing import Optional
from app.domain.entities.user import User, UserRole
from app.repository.user_repository import UserRepository
from app.use_cases.exceptions import UserNotFoundError
from app.core.security import get_password_hash

class UpdateUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(
        self, 
        user_id: UUID, 
        name: Optional[str] = None,
        surname: Optional[str] = None,
        email: Optional[str] = None,
        age: Optional[int] = None,
        phone: Optional[str] = None,
        role: Optional[UserRole] = None,
        password: Optional[str] = None,
        disabled: Optional[bool] = None
    ) -> User:
        # Проверяем существование пользователя
        existing_user = await self.user_repository.get(id=user_id)
        if not existing_user:
            raise UserNotFoundError(user_id)
        
        # Подготавливаем данные для обновления
        updates = {}
        if name is not None:
            updates["name"] = name
        if surname is not None:
            updates["surname"] = surname
        if email is not None:
            updates["email"] = email
        if age is not None:
            updates["age"] = age
        if phone is not None:
            updates["phone"] = phone
        if role is not None:
            updates["role"] = role
        if password is not None:
            updates["hashed_password"] = get_password_hash(password)
        if disabled is not None:
            updates["disabled"] = disabled
        
        # Обновляем пользователя
        updated_user = await self.user_repository.update(str(user_id), **updates)
        if not updated_user:
            raise UserNotFoundError(user_id)
        
        return updated_user