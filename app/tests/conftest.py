import sys
import pytest
import os
from unittest.mock import patch

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Патчим security для тестов
from app.core.test_security import get_password_hash, verify_password
patch('app.use_cases.auth.get_password_hash', get_password_hash).start()
patch('app.use_cases.auth.verify_password', verify_password).start()
patch('app.core.security.get_password_hash', get_password_hash).start()
patch('app.core.security.verify_password', verify_password).start()

from app.use_cases.crud_doctor import GetDoctor

class InMemoryDoctorRepository:
    def __init__(self):
        self.doctors = []
    
    async def get(self, **filters):
        for doctor in self.doctors:
            if doctor.id == filters.get('id'):
                return doctor
        return None
    
    async def add(self, doctor):
        self.doctors.append(doctor)
    
    async def list_all(self, skip=0, limit=100):
        return self.doctors[skip:skip+limit]

@pytest.fixture
def doctor_repository():
    return InMemoryDoctorRepository()

@pytest.fixture
def get_doctor(doctor_repository):
    return GetDoctor(doctor_repository)