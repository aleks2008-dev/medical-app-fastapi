import sys
sys.path.insert(0, '/app')

import uuid
import pytest
from app.domain.entities.doctor import Doctor
from app.use_cases.crud_doctor import GetDoctor
from app.use_cases.exceptions import DoctorNotFoundError

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

@pytest.mark.asyncio
async def test_doctor_not_found():
    repository = InMemoryDoctorRepository()
    use_case = GetDoctor(repository)
    
    non_existent_doctor_id = uuid.uuid4()
    with pytest.raises(DoctorNotFoundError):
        await use_case(non_existent_doctor_id)
    print('Doctor not found test passed')

@pytest.mark.asyncio
async def test_create_and_get_doctor():
    repository = InMemoryDoctorRepository()
    use_case = GetDoctor(repository)
    
    from app.domain.entities.doctor import CategoryEnum
    doctor = Doctor(name='Test', surname='Doctor', age=30, specialization='GP', category=CategoryEnum.FIRST, password='test123')
    await repository.add(doctor)
    
    found_doctor = await use_case(doctor.id)
    assert found_doctor.name == 'Test'
    assert found_doctor.surname == 'Doctor'
    print('Doctor creation test passed')

@pytest.mark.asyncio
async def test_list_doctors():
    repository = InMemoryDoctorRepository()
    
    from app.domain.entities.doctor import CategoryEnum
    doctor1 = Doctor(name='Doctor1', surname='Test', age=30, specialization='GP', category=CategoryEnum.FIRST, password='test123')
    doctor2 = Doctor(name='Doctor2', surname='Test', age=35, specialization='Cardio', category=CategoryEnum.SECOND, password='test123')
    
    await repository.add(doctor1)
    await repository.add(doctor2)
    
    doctors = await repository.list_all()
    assert len(doctors) == 2
    assert {d.name for d in doctors} == {'Doctor1', 'Doctor2'}
    print('List doctors test passed')

if __name__ == '__main__':
    import asyncio
    asyncio.run(test_doctor_not_found())
    asyncio.run(test_create_and_get_doctor())
    asyncio.run(test_list_doctors())
    print('All InMemory tests passed!')

