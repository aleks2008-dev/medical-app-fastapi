import pytest
from uuid import UUID, uuid4
from datetime import datetime
from app.domain.entities.appointment import Appointment

def test_appointment_creation():
    doctor_id = uuid4()
    user_id = uuid4()
    room_id = uuid4()
    appointment_datetime = datetime(2024, 12, 25, 14, 30)
    
    appointment = Appointment(
        datetime=appointment_datetime,
        doctor_id=doctor_id,
        user_id=user_id,
        room_id=room_id
    )
    
    assert appointment.datetime == appointment_datetime
    assert appointment.doctor_id == doctor_id
    assert appointment.user_id == user_id
    assert appointment.room_id == room_id
    assert isinstance(appointment.id, UUID)

def test_appointment_to_dict():
    doctor_id = uuid4()
    user_id = uuid4()
    room_id = uuid4()
    appointment_datetime = datetime(2024, 12, 25, 14, 30)
    
    appointment = Appointment(
        datetime=appointment_datetime,
        doctor_id=doctor_id,
        user_id=user_id,
        room_id=room_id
    )
    
    appointment_dict = appointment.to_dict()
    
    assert appointment_dict["datetime"] == appointment_datetime
    assert appointment_dict["doctor_id"] == str(doctor_id)
    assert appointment_dict["user_id"] == str(user_id)
    assert appointment_dict["room_id"] == str(room_id)
    assert "uuid" in appointment_dict

def test_appointment_from_dict():
    doctor_id = "550e8400-e29b-41d4-a716-446655440001"
    user_id = "550e8400-e29b-41d4-a716-446655440002"
    room_id = "550e8400-e29b-41d4-a716-446655440003"
    appointment_uuid = "550e8400-e29b-41d4-a716-446655440000"
    
    data = {
        "datetime": datetime(2024, 12, 25, 14, 30),
        "doctor_id": doctor_id,
        "user_id": user_id,
        "room_id": room_id,
        "uuid": appointment_uuid
    }
    
    appointment = Appointment.from_dict(data)
    
    assert appointment.datetime == datetime(2024, 12, 25, 14, 30)
    assert str(appointment.doctor_id) == doctor_id
    assert str(appointment.user_id) == user_id
    assert str(appointment.room_id) == room_id
    assert str(appointment.id) == appointment_uuid