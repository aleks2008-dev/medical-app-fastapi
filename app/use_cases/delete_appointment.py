from uuid import UUID
from app.repository.appointment_repository import AppointmentRepository
from app.use_cases.exceptions import AppointmentNotFoundError

class DeleteAppointment:
    def __init__(self, appointment_repository: AppointmentRepository):
        self.appointment_repository = appointment_repository

    async def __call__(self, appointment_id: UUID) -> bool:
        # Проверяем существование записи
        existing_appointment = await self.appointment_repository.get(id=appointment_id)
        if not existing_appointment:
            raise AppointmentNotFoundError(appointment_id)
        
        # Удаляем запись
        return await self.appointment_repository.delete(str(appointment_id))