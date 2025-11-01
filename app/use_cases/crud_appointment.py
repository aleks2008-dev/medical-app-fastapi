from uuid import UUID
from app.domain.entities.appointment import Appointment
from app.repository.appointment_repository import AppointmentRepository
from app.use_cases.exceptions import AppointmentNotFoundError

class GetAppointment:
    def __init__(self, appointment_repository: AppointmentRepository):
        self.appointment_repository = appointment_repository

    async def __call__(self, appointment_id: UUID) -> Appointment:
        appointment = await self.appointment_repository.get(id=appointment_id)
        if not appointment:
            raise AppointmentNotFoundError(appointment_id)
        return appointment

class CreateAppointment:
    def __init__(self, appointment_repository: AppointmentRepository):
        self.appointment_repository = appointment_repository

    async def __call__(self, appointment: Appointment) -> Appointment:
        await self.appointment_repository.add(appointment)  # This is equivalent to await MongoDoctorRepository().add(doctor)
        return appointment

class ListAppointments:
    def __init__(self, appointment_repository: AppointmentRepository):
        self.appointment_repository = appointment_repository

    async def __call__(self, skip: int = 0, limit: int = 100) -> list[Appointment]:
        return await self.appointment_repository.list_all(skip=skip, limit=limit)
    
    