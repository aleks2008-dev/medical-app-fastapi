from uuid import UUID
from app.domain.entities.user import User
from app.repository.user_repository import UserRepository
from app.domain.interfaces.password_hasher import PasswordHasher
from app.use_cases.exceptions import UserNotFoundError

class GetUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID) -> User:
        user = await self.user_repository.get(id=user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

class CreateUser:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def __call__(self, user_data, plain_password: str) -> User:
        hashed_password = self.password_hasher.hash(plain_password)
        user = user_data.to_entity(hashed_password)
        await self.user_repository.add(user)
        return user

class ListUsers:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.user_repository.list_all(skip=skip, limit=limit)