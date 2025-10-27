import pytest
from uuid import UUID
from app.domain.entities.user import User, UserRole

def test_user_creation():
    user = User(
        name="John",
        surname="Doe",
        email="john@example.com",
        hashed_password="hashed_password",
        role=UserRole.user
    )
    
    assert user.name == "John"
    assert user.surname == "Doe"
    assert user.email == "john@example.com"
    assert user.role == UserRole.user
    assert isinstance(user.id, UUID)
    assert not user.disabled

def test_user_to_dict():
    user = User(
        name="Jane",
        surname="Smith",
        email="jane@example.com",
        hashed_password="hashed_password",
        age=25,
        phone="+1234567890",
        role=UserRole.admin
    )
    
    user_dict = user.to_dict()
    
    assert user_dict["name"] == "Jane"
    assert user_dict["surname"] == "Smith"
    assert user_dict["email"] == "jane@example.com"
    assert user_dict["age"] == 25
    assert user_dict["phone"] == "+1234567890"
    assert user_dict["role"] == "admin"
    assert "uuid" in user_dict

def test_user_from_dict():
    data = {
        "name": "Bob",
        "surname": "Johnson",
        "email": "bob@example.com",
        "hashed_password": "hashed_password",
        "age": 30,
        "role": "doctor",
        "disabled": False,
        "uuid": "550e8400-e29b-41d4-a716-446655440000"
    }
    
    user = User.from_dict(data)
    
    assert user.name == "Bob"
    assert user.surname == "Johnson"
    assert user.email == "bob@example.com"
    assert user.age == 30
    assert user.role == UserRole.doctor
    assert not user.disabled
    assert str(user.id) == "550e8400-e29b-41d4-a716-446655440000"