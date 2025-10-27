import pytest
from uuid import uuid4
from app.use_cases.exceptions import DoctorNotFoundError, UserNotFoundError

def test_doctor_not_found_error():
    doctor_id = uuid4()
    error = DoctorNotFoundError(doctor_id)
    
    assert str(doctor_id) in str(error)
    assert "Doctor" in str(error)
    assert "not found" in str(error)

def test_user_not_found_error():
    user_id = uuid4()
    error = UserNotFoundError(user_id)
    
    assert str(user_id) in str(error)
    assert "User" in str(error)
    assert "not found" in str(error)

def test_doctor_not_found_error_inheritance():
    doctor_id = uuid4()
    error = DoctorNotFoundError(doctor_id)
    
    assert isinstance(error, Exception)

def test_user_not_found_error_inheritance():
    user_id = uuid4()
    error = UserNotFoundError(user_id)
    
    assert isinstance(error, Exception)