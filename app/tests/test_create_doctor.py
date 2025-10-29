import pytest
from app.use_cases.crud_doctor import CreateDoctor
from tests.utils import create_doctor

@pytest.mark.asyncio
async def test_create_doctor_use_case(doctor_repository):
    create_doctor_use_case = CreateDoctor(doctor_repository)
    
    doctor_data = create_doctor(
        name="Елена",
        surname="Волкова", 
        age=31,
        specialization="Невролог"
    )
    
    doctor = await create_doctor_use_case(doctor_data)
    
    assert doctor.name == "Елена"
    assert doctor.surname == "Волкова"
    assert doctor.age == 31
    assert doctor.specialization == "Невролог"
    
    # Check that doctor was saved in repository
    saved_doctor = await doctor_repository.get(id=doctor.id)
    assert saved_doctor is not None
    assert saved_doctor.name == "Елена"

@pytest.mark.asyncio
async def test_list_doctors_with_pagination(doctor_repository):
    from app.use_cases.crud_doctor import ListDoctors
    
    list_doctors_use_case = ListDoctors(doctor_repository)
    
    # Add 3 doctors
    for i in range(3):
        doctor = create_doctor(name=f"Доктор{i}")
        await doctor_repository.add(doctor)
    
    # Test pagination
    doctors_page1 = await list_doctors_use_case(skip=0, limit=2)
    doctors_page2 = await list_doctors_use_case(skip=2, limit=2)
    
    assert len(doctors_page1) == 2
    assert len(doctors_page2) == 1