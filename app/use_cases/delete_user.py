from uuid import UUID
from app.repository.user_repository import UserRepository
from app.use_cases.exceptions import UserNotFoundError

class DeleteUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID) -> bool:
        # Проверяем существование пользователя
        existing_user = await self.user_repository.get(id=user_id)
        if not existing_user:
            raise UserNotFoundError(user_id)
        
        # Удаляем пользователя
        return await self.user_repository.delete(str(user_id))