import pytest
from uuid import uuid4, UUID
from app.use_cases.delete_user import DeleteUser
from app.use_cases.exceptions import UserNotFoundError
from app.domain.entities.user import User, UserRole

def create_user(name="John", surname="Doe", email="john@example.com", **kwargs):
    return User(
        name=name,
        surname=surname,
        email=email,
        hashed_password="hashed_password",
        role=kwargs.get('role', UserRole.user),
        uuid=kwargs.get('uuid', uuid4())
    )

class MockUserRepository:
    def __init__(self):
        self.users = {}
    
    async def get(self, **filters):
        user_id = filters.get('id')
        return self.users.get(user_id)
    
    async def add(self, user):
        self.users[user.id] = user
    
    async def delete(self, user_id: str) -> bool:
        user_uuid = UUID(user_id)
        if user_uuid in self.users:
            del self.users[user_uuid]
            return True
        return False

@pytest.fixture
def user_repository():
    return MockUserRepository()

@pytest.fixture
def delete_user_use_case(user_repository):
    return DeleteUser(user_repository)

@pytest.mark.asyncio
async def test_delete_user_success(delete_user_use_case, user_repository):
    # Создаем пользователя
    user = create_user(name="John", surname="Doe")
    await user_repository.add(user)
    
    # Удаляем пользователя
    result = await delete_user_use_case(user.id)
    
    assert result is True
    
    # Проверяем что пользователь удален
    deleted_user = await user_repository.get(id=user.id)
    assert deleted_user is None

@pytest.mark.asyncio
async def test_delete_nonexistent_user(delete_user_use_case):
    nonexistent_id = uuid4()
    
    with pytest.raises(UserNotFoundError):
        await delete_user_use_case(nonexistent_id)