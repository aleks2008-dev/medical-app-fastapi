from typing import Any, Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repository.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.database.models import UserORM


class DatabaseException(Exception):
    def __str__(self):
        return "Database is not currently available. Please try again later."


class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, **filters: Any) -> Optional[User]:
        try:
            query = select(UserORM)
            
            if user_id := filters.get('id'):
                query = query.where(UserORM.id == user_id)
            
            result = await self.session.execute(query)
            user_db = result.scalar_one_or_none()
            
            return self._to_entity(user_db) if user_db else None
            
        except Exception as e:
            print(f'PostgreSQL get error: {e}')
            raise DatabaseException

    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            query = select(UserORM).where(UserORM.email == email)
            result = await self.session.execute(query)
            user_db = result.scalar_one_or_none()
            
            return self._to_entity(user_db) if user_db else None
            
        except Exception as e:
            print(f'PostgreSQL get_by_email error: {e}')
            raise DatabaseException

    async def add(self, user: User) -> None:
        try:
            user_db = UserORM(
                id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                age=user.age,
                phone=user.phone,
                role=user.role,
                hashed_password=user.hashed_password,
                disabled=user.disabled
            )
            self.session.add(user_db)
            await self.session.commit()
            
        except Exception:
            await self.session.rollback()
            raise DatabaseException

    async def update(self, user_id: str, **updates: Any) -> Optional[User]:
        try:
            query = select(UserORM).where(UserORM.id == UUID(user_id))
            result = await self.session.execute(query)
            user_db = result.scalar_one_or_none()
            
            if not user_db:
                return None
            
            for key, value in updates.items():
                if value is not None and hasattr(user_db, key):
                    setattr(user_db, key, value)
            
            await self.session.commit()
            return self._to_entity(user_db)
            
        except Exception as e:
            await self.session.rollback()
            print(f'PostgreSQL update error: {e}')
            raise DatabaseException

    async def delete(self, user_id: str) -> bool:
        try:
            query = select(UserORM).where(UserORM.id == UUID(user_id))
            result = await self.session.execute(query)
            user_db = result.scalar_one_or_none()
            
            if user_db:
                await self.session.delete(user_db)
                await self.session.commit()
                return True
            return False
            
        except Exception as e:
            await self.session.rollback()
            print(f'PostgreSQL delete error: {e}')
            raise DatabaseException

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        try:
            query = select(UserORM).offset(skip).limit(limit)
            result = await self.session.execute(query)
            users_db = result.scalars().all()
            
            return [self._to_entity(user_db) for user_db in users_db]
            
        except Exception as e:
            print(f'PostgreSQL list_all error: {e}')
            raise DatabaseException

    def _to_entity(self, user_db: UserORM) -> User:
        return User(
            name=user_db.name,
            surname=user_db.surname,
            email=user_db.email,
            age=user_db.age,
            phone=user_db.phone,
            role=user_db.role,
            hashed_password=user_db.hashed_password,
            disabled=user_db.disabled,
            reset_token=user_db.reset_token,
            reset_token_expires=user_db.reset_token_expires,
            uuid=user_db.id
        )
    
    