from uuid import UUID
from app.domain.entities.doctor import Doctor
from app.repository.doctor_repository import DoctorRepository
from app.use_cases.exceptions import DoctorNotFoundError

class GetDoctor:
    def __init__(self, doctor_repository: DoctorRepository):
        self.doctor_repository = doctor_repository

    async def __call__(self, doctor_id: UUID) -> Doctor:
        doctor = await self.doctor_repository.get(id=doctor_id)
        if not doctor:
            raise DoctorNotFoundError(doctor_id)
        return doctor

class CreateDoctor:
    def __init__(self, doctor_repository: DoctorRepository):
        self.doctor_repository = doctor_repository

    async def __call__(self, doctor: Doctor) -> Doctor:
        await self.doctor_repository.add(doctor)  # Это равносильно
                            # await MongoDoctorRepository().add(doctor)
        return doctor

class ListDoctors:
    def __init__(self, doctor_repository: DoctorRepository):
        self.doctor_repository = doctor_repository

    async def __call__(self, skip: int = 0, limit: int = 100) -> list[Doctor]:
        return await self.doctor_repository.list_all(skip=skip, limit=limit)
    
    