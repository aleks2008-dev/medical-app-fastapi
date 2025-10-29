import pytest
from unittest.mock import AsyncMock, patch
from app.use_cases.auth import AuthService
from app.domain.entities.user import User, UserRole
from app.core.test_security import get_password_hash, verify_password
from fastapi import HTTPException

class MockUserRepository:
    def __init__(self):
        self.users = {}
    
    async def get_by_email(self, email: str):
        return self.users.get(email)
    
    async def add(self, user: User):
        self.users[user.email] = user
    
    async def get(self, **filters):
        user_id = filters.get('id')
        for user in self.users.values():
            if user.id == user_id:
                return user
        return None
    
    async def update(self, user_id: str, **updates):
        for user in self.users.values():
            if str(user.id) == user_id:
                for key, value in updates.items():
                    setattr(user, key, value)
                return user
        return None

@pytest.fixture
def user_repository():
    return MockUserRepository()

class MockPasswordHasher:
    def hash(self, password: str) -> str:
        return get_password_hash(password)
    
    def verify(self, password: str, hashed: str) -> bool:
        return verify_password(password, hashed)

@pytest.fixture
def auth_service(user_repository):
    password_hasher = MockPasswordHasher()
    return AuthService(user_repository, password_hasher)

@pytest.mark.asyncio
async def test_register_user(auth_service):
    user = await auth_service.register_user(
        name="John",
        surname="Doe", 
        email="john@example.com",
        password="password123"
    )
    
    assert user.name == "John"
    assert user.email == "john@example.com"
    assert user.role == UserRole.user
    assert verify_password("password123", user.hashed_password)

@pytest.mark.asyncio
async def test_register_existing_user(auth_service):
    # Register user
    await auth_service.register_user(
        name="John",
        surname="Doe",
        email="john@example.com", 
        password="password123"
    )
    
    # Try to register with the same email
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.register_user(
            name="Jane",
            surname="Doe",
            email="john@example.com",
            password="password456"
        )
    
    assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_authenticate_user(auth_service):
    # Create user
    user = await auth_service.register_user(
        name="John",
        surname="Doe",
        email="john@example.com",
        password="password123"
    )
    
    # Authenticate
    authenticated_user = await auth_service.authenticate_user("john@example.com", "password123")
    assert authenticated_user.id == user.id

@pytest.mark.asyncio
async def test_authenticate_wrong_password(auth_service):
    await auth_service.register_user(
        name="John",
        surname="Doe",
        email="john@example.com",
        password="password123"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.authenticate_user("john@example.com", "wrongpassword")
    
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_authenticate_nonexistent_user(auth_service):
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.authenticate_user("nonexistent@example.com", "password123")
    
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
@patch('app.use_cases.auth.send_reset_email')
async def test_request_password_reset(mock_send_email, auth_service):
    mock_send_email.return_value = None
    
    await auth_service.register_user(
        name="John",
        surname="Doe",
        email="john@example.com",
        password="password123"
    )
    
    result = await auth_service.request_password_reset("john@example.com")
    assert "reset email will be sent" in result["message"]
    mock_send_email.assert_called_once()

@pytest.mark.asyncio
async def test_request_password_reset_nonexistent_user(auth_service):
    result = await auth_service.request_password_reset("nonexistent@example.com")
    assert "reset email will be sent" in result["message"]