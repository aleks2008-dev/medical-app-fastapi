from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
from app.core.security import verify_token
from app.repository.user_repository import UserRepository
from app.adapters.postgres_user_repository import PostgresUserRepository
from app.infrastructure.database.postgres import get_db
from app.domain.entities.user import User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()

async def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return PostgresUserRepository(session)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository)
) -> User:
    token = credentials.credentials
    user_id = await verify_token(token)
    
    user = await user_repository.get(id=UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is disabled"
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def get_doctor_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role not in [UserRole.doctor, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user