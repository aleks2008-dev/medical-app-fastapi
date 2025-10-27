from uuid import UUID
from app.domain.entities.user import User
from app.repository.user_repository import UserRepository
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
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user: User) -> User:
        await self.user_repository.add(user)  # Это равносильно
                            # await MongoDoctorRepository().add(doctor)
        return user

class ListUsers:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.user_repository.list_all(skip=skip, limit=limit)