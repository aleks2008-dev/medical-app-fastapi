from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings
from app.core.token_storage import token_storage

pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__truncate_error=True
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt не может проверять пароли длиннее 72 байт
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # bcrypt не может хешировать пароли длиннее 72 байт
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    # Сохраняем токен в Redis
    user_id = data.get("sub")
    if user_id:
        await token_storage.store_refresh_token(user_id, encoded_jwt)
    
    return encoded_jwt

async def verify_token(token: str):
    try:
        # Проверяем, не в черном списке ли токен
        if await token_storage.is_token_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )
        
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def create_reset_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def verify_reset_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None

async def revoke_token(token: str):
    """Добавить токен в черный список"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        exp = datetime.fromtimestamp(payload.get("exp"))
        await token_storage.store_blacklisted_token(token, exp)
    except JWTError:
        pass

async def verify_refresh_token(token: str, user_id: str) -> bool:
    """Проверить валидность refresh токена"""
    stored_token = await token_storage.get_refresh_token(user_id)
    return stored_token == token