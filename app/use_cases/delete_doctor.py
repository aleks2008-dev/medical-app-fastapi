from uuid import UUID
from app.repository.doctor_repository import DoctorRepository
from app.use_cases.exceptions import DoctorNotFoundError

class DeleteDoctor:
    def __init__(self, doctor_repository: DoctorRepository):
        self.doctor_repository = doctor_repository

    async def __call__(self, doctor_id: UUID) -> bool:
        # Chek existin doctor
        existing_doctor = await self.doctor_repository.get(id=doctor_id)
        if not existing_doctor:
            raise DoctorNotFoundError(doctor_id)
        
        # Delete doctor
        return await self.doctor_repository.delete(str(doctor_id))