import pytest
from uuid import uuid4, UUID
from app.use_cases.delete_doctor import DeleteDoctor
from app.use_cases.exceptions import DoctorNotFoundError
from app.tests.utils import create_doctor

class MockDoctorRepository:
    def __init__(self):
        self.doctors = {}
    
    async def get(self, **filters):
        doctor_id = filters.get('id')
        return self.doctors.get(doctor_id)
    
    async def add(self, doctor):
        self.doctors[doctor.id] = doctor
    
    async def delete(self, doctor_id: str) -> bool:
        doctor_uuid = UUID(doctor_id)
        if doctor_uuid in self.doctors:
            del self.doctors[doctor_uuid]
            return True
        return False

@pytest.fixture
def doctor_repository():
    return MockDoctorRepository()

@pytest.fixture
def delete_doctor_use_case(doctor_repository):
    return DeleteDoctor(doctor_repository)

@pytest.mark.asyncio
async def test_delete_doctor_success(delete_doctor_use_case, doctor_repository):
    # Создаем врача
    doctor = create_doctor(name="John", surname="Doe")
    await doctor_repository.add(doctor)
    
    # Удаляем врача
    result = await delete_doctor_use_case(doctor.id)
    
    assert result is True
    
    # Проверяем что врач удален
    deleted_doctor = await doctor_repository.get(id=doctor.id)
    assert deleted_doctor is None

@pytest.mark.asyncio
async def test_delete_nonexistent_doctor(delete_doctor_use_case):
    nonexistent_id = uuid4()
    
    with pytest.raises(DoctorNotFoundError):
        await delete_doctor_use_case(nonexistent_id)