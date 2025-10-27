import pytest
from uuid import uuid4, UUID
from app.use_cases.update_doctor import UpdateDoctor
from app.domain.entities.doctor import Doctor, CategoryEnum
from app.use_cases.exceptions import DoctorNotFoundError
from app.tests.utils import create_doctor

class MockDoctorRepository:
    def __init__(self):
        self.doctors = {}
    
    async def get(self, **filters):
        doctor_id = filters.get('id')
        return self.doctors.get(doctor_id)
    
    async def add(self, doctor: Doctor):
        self.doctors[doctor.id] = doctor
    
    async def update(self, doctor_id: str, **updates):
        doctor = self.doctors.get(UUID(doctor_id))
        if not doctor:
            return None
        
        for key, value in updates.items():
            if hasattr(doctor, key):
                setattr(doctor, key, value)
        
        return doctor

@pytest.fixture
def doctor_repository():
    return MockDoctorRepository()

@pytest.fixture
def update_doctor_use_case(doctor_repository):
    return UpdateDoctor(doctor_repository)

@pytest.mark.asyncio
async def test_update_doctor_success(update_doctor_use_case, doctor_repository):
    # Создаем врача
    doctor = create_doctor(name="John", surname="Doe")
    await doctor_repository.add(doctor)
    
    # Обновляем врача
    updated_doctor = await update_doctor_use_case(
        doctor_id=doctor.id,
        name="Jane",
        age=35,
        specialization="Cardiology"
    )
    
    assert updated_doctor.name == "Jane"
    assert updated_doctor.age == 35
    assert updated_doctor.specialization == "Cardiology"
    assert updated_doctor.surname == "Doe"  # Не изменилось

@pytest.mark.asyncio
async def test_update_nonexistent_doctor(update_doctor_use_case):
    nonexistent_id = uuid4()
    
    with pytest.raises(DoctorNotFoundError):
        await update_doctor_use_case(
            doctor_id=nonexistent_id,
            name="Jane"
        )

@pytest.mark.asyncio
async def test_update_doctor_partial(update_doctor_use_case, doctor_repository):
    # Создаем врача
    doctor = create_doctor(name="John", surname="Doe", age=30)
    await doctor_repository.add(doctor)
    
    # Обновляем только имя
    updated_doctor = await update_doctor_use_case(
        doctor_id=doctor.id,
        name="Jane"
    )
    
    assert updated_doctor.name == "Jane"
    assert updated_doctor.surname == "Doe"  # Не изменилось
    assert updated_doctor.age == 30  # Не изменилось

@pytest.mark.asyncio
async def test_update_doctor_category(update_doctor_use_case, doctor_repository):
    # Создаем врача
    doctor = create_doctor(category=CategoryEnum.FIRST)
    await doctor_repository.add(doctor)
    
    # Обновляем категорию
    updated_doctor = await update_doctor_use_case(
        doctor_id=doctor.id,
        category=CategoryEnum.HIGHEST
    )
    
    assert updated_doctor.category == CategoryEnum.HIGHEST