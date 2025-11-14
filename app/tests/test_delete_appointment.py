import pytest
from uuid import uuid4, UUID
from datetime import datetime
from app.use_cases.delete_appointment import DeleteAppointment
from app.use_cases.exceptions import AppointmentNotFoundError
from app.domain.entities.appointment import Appointment

def create_appointment(**kwargs):
    return Appointment(
        datetime=kwargs.get('datetime', datetime(2024, 12, 25, 10, 0)),
        doctor_id=kwargs.get('doctor_id', uuid4()),
        user_id=kwargs.get('user_id', uuid4()),
        room_id=kwargs.get('room_id', uuid4()),
        uuid=kwargs.get('uuid', uuid4())
    )

class MockAppointmentRepository:
    def __init__(self):
        self.appointments = {}
    
    async def get(self, **filters):
        appointment_id = filters.get('id')
        return self.appointments.get(appointment_id)
    
    async def add(self, appointment):
        self.appointments[appointment.id] = appointment
    
    async def delete(self, appointment_id: str) -> bool:
        appointment_uuid = UUID(appointment_id)
        if appointment_uuid in self.appointments:
            del self.appointments[appointment_uuid]
            return True
        return False

@pytest.fixture
def appointment_repository():
    return MockAppointmentRepository()

@pytest.fixture
def delete_appointment_use_case(appointment_repository):
    return DeleteAppointment(appointment_repository)

@pytest.mark.asyncio
async def test_delete_appointment_success(delete_appointment_use_case, appointment_repository):
    # Create appointment
    appointment = create_appointment()
    await appointment_repository.add(appointment)
    
    # Delete appointment
    result = await delete_appointment_use_case(appointment.id)
    
    assert result is True
    
    # Chek what appointment delete
    deleted_appointment = await appointment_repository.get(id=appointment.id)
    assert deleted_appointment is None

@pytest.mark.asyncio
async def test_delete_nonexistent_appointment(delete_appointment_use_case):
    nonexistent_id = uuid4()
    
    with pytest.raises(AppointmentNotFoundError):
        await delete_appointment_use_case(nonexistent_id)