import pytest
from uuid import UUID
from app.domain.entities.doctor import Doctor, CategoryEnum

def test_doctor_creation():
    doctor = Doctor(
        name="Иван",
        surname="Петров", 
        age=35,
        specialization="Кардиолог",
        category=CategoryEnum.FIRST,
        password="password123"
    )
    
    assert doctor.name == "Иван"
    assert doctor.surname == "Петров"
    assert doctor.age == 35
    assert doctor.specialization == "Кардиолог"
    assert isinstance(doctor.id, UUID)

def test_doctor_to_dict():
    doctor = Doctor(
        name="Анна",
        surname="Сидорова",
        age=28,
        specialization="Терапевт",
        category=CategoryEnum.SECOND,
        password="password123"
    )
    
    doctor_dict = doctor.to_dict()
    
    assert doctor_dict["name"] == "Анна"
    assert doctor_dict["surname"] == "Сидорова"
    assert doctor_dict["age"] == 28
    assert doctor_dict["specialization"] == "Терапевт"
    assert "uuid" in doctor_dict

def test_doctor_from_dict():
    data = {
        "name": "Михаил",
        "surname": "Козлов",
        "age": 42,
        "specialization": "Хирург",
        "category": "first",
        "password": "password123",
        "uuid": "550e8400-e29b-41d4-a716-446655440000"
    }
    
    doctor = Doctor.from_dict(data)
    
    assert doctor.name == "Михаил"
    assert doctor.surname == "Козлов"
    assert doctor.age == 42
    assert doctor.specialization == "Хирург"
    assert str(doctor.id) == "550e8400-e29b-41d4-a716-446655440000"