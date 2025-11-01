import pytest
from uuid import uuid4, UUID
from app.use_cases.update_user import UpdateUser
from app.domain.entities.user import User, UserRole
from app.use_cases.exceptions import UserNotFoundError

def create_user(name="John", surname="Doe", email="john@example.com", **kwargs):
    return User(
        name=name,
        surname=surname,
        email=email,
        hashed_password="hashed_password",
        role=kwargs.get('role', UserRole.user),
        age=kwargs.get('age', 30),
        phone=kwargs.get('phone'),
        disabled=kwargs.get('disabled', False),
        uuid=kwargs.get('uuid', uuid4())
    )

class MockUserRepository:
    def __init__(self):
        self.users = {}
    
    async def get(self, **filters):
        user_id = filters.get('id')
        return self.users.get(user_id)
    
    async def add(self, user: User):
        self.users[user.id] = user
    
    async def update(self, user_id: str, **updates):
        user = self.users.get(UUID(user_id))
        if not user:
            return None
        
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        return user

@pytest.fixture
def user_repository():
    return MockUserRepository()

@pytest.fixture
def update_user_use_case(user_repository):
    return UpdateUser(user_repository)

@pytest.mark.asyncio
async def test_update_user_success(update_user_use_case, user_repository):
    # Create user
    user = create_user(name="John", surname="Doe")
    await user_repository.add(user)
    
    # Update user
    updated_user = await update_user_use_case(
        user_id=user.id,
        name="Jane",
        age=25,
        phone="+1234567890"
    )
    
    assert updated_user.name == "Jane"
    assert updated_user.age == 25
    assert updated_user.phone == "+1234567890"
    assert updated_user.surname == "Doe"  # Not changed

@pytest.mark.asyncio
async def test_update_nonexistent_user(update_user_use_case):
    nonexistent_id = uuid4()
    
    with pytest.raises(UserNotFoundError):
        await update_user_use_case(
            user_id=nonexistent_id,
            name="Jane"
        )

@pytest.mark.asyncio
async def test_update_user_role(update_user_use_case, user_repository):
    # Create user
    user = create_user(role=UserRole.user)
    await user_repository.add(user)
    
    # Update role
    updated_user = await update_user_use_case(
        user_id=user.id,
        role=UserRole.admin
    )
    
    assert updated_user.role == UserRole.admin

@pytest.mark.asyncio
async def test_update_user_disable(update_user_use_case, user_repository):
    # Create user
    user = create_user(disabled=False)
    await user_repository.add(user)
    
    # Disconected user
    updated_user = await update_user_use_case(
        user_id=user.id,
        disabled=True
    )
    
    assert updated_user.disabled is True