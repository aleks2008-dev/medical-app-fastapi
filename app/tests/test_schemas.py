import pytest
from pydantic import ValidationError
from datetime import date
from uuid import uuid4
from app.api.routers.schema import (
    DoctorItemCreate, 
    UserItemCreate, 
    AppointmentItemCreate,
    CategoryEnum,
    UserRole
)

def test_doctor_item_create_valid():
    doctor_data = {
        "name": "John",
        "surname": "Doe",
        "age": 35,
        "specialization": "Cardiology",
        "category": CategoryEnum.FIRST,
        "password": "password123"
    }
    
    doctor = DoctorItemCreate(**doctor_data)
    assert doctor.name == "John"
    assert doctor.age == 35
    assert doctor.category == CategoryEnum.FIRST

def test_doctor_item_create_invalid_age():
    with pytest.raises(ValidationError):
        DoctorItemCreate(
            name="John",
            surname="Doe",
            age=-5,  # Invalid age
            specialization="Cardiology",
            category=CategoryEnum.FIRST,
            password="password123"
        )

def test_doctor_item_create_short_name():
    with pytest.raises(ValidationError):
        DoctorItemCreate(
            name="Jo",  # short name
            surname="Doe",
            age=35,
            specialization="Cardiology",
            category=CategoryEnum.FIRST,
            password="password123"
        )

def test_user_item_create_valid():
    user_data = {
        "name": "Jane",
        "surname": "Smith",
        "email": "jane@example.com",
        "password": "password123",
        "age": 28
    }
    
    user = UserItemCreate(**user_data)
    assert user.name == "Jane"
    assert user.email == "jane@example.com"

def test_user_item_create_invalid_email():
    with pytest.raises(ValidationError):
        UserItemCreate(
            name="Jane",
            surname="Smith",
            email="invalid-email",  # Invalid email
            password="password123"
        )

def test_appointment_item_create_valid():
    appointment_data = {
        "date": date(2024, 12, 25),
        "doctor_id": uuid4(),
        "user_id": uuid4(),
        "room_id": uuid4()
    }
    
    appointment = AppointmentItemCreate(**appointment_data)
    assert appointment.date == date(2024, 12, 25)
    assert isinstance(appointment.doctor_id, type(uuid4()))

def test_appointment_date_from_int():
    appointment_data = {
        "date": 20241225,  # YYYYMMDD format
        "doctor_id": uuid4(),
        "user_id": uuid4(),
        "room_id": uuid4()
    }
    
    appointment = AppointmentItemCreate(**appointment_data)
    assert appointment.date == date(2024, 12, 25)

def test_category_enum_values():
    assert CategoryEnum.FIRST == "first"
    assert CategoryEnum.SECOND == "second"
    assert CategoryEnum.HIGHEST == "highest"
    assert CategoryEnum.NO_CATEGORY == "no_category"

def test_user_role_enum_values():
    assert UserRole.user == "user"
    assert UserRole.admin == "admin"
    assert UserRole.doctor == "doctor"