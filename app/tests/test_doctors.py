import uuid
import pytest
from app.use_cases.exceptions import DoctorNotFoundError
from app.tests.utils import create_doctor

@pytest.mark.asyncio
async def test_doctor_not_found(get_doctor):
    non_existent_doctor_id = uuid.uuid4()
    with pytest.raises(DoctorNotFoundError):
        await get_doctor(non_existent_doctor_id)

@pytest.mark.asyncio
async def test_create_and_get_doctor(doctor_repository, get_doctor):
    # Create doctor
    doctor = create_doctor(name="Test", surname="Doctor")
    await doctor_repository.add(doctor)
    
    # Get doctor
    found_doctor = await get_doctor(doctor.id)
    assert found_doctor.name == "Test"
    assert found_doctor.surname == "Doctor"
    assert found_doctor.id == doctor.id

@pytest.mark.asyncio
async def test_list_doctors(doctor_repository):
    # Add multiple doctors
    doctor1 = create_doctor(name="Doctor1")
    doctor2 = create_doctor(name="Doctor2")
    
    await doctor_repository.add(doctor1)
    await doctor_repository.add(doctor2)
    
    # List doctors
    doctors = await doctor_repository.list_all()
    assert len(doctors) == 2
    assert {d.name for d in doctors} == {"Doctor1", "Doctor2"}
    