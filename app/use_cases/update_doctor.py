from uuid import UUID
from typing import Optional
from app.domain.entities.doctor import Doctor, CategoryEnum
from app.repository.doctor_repository import DoctorRepository
from app.use_cases.exceptions import DoctorNotFoundError
from app.core.security import get_password_hash

class UpdateDoctor:
    def __init__(self, doctor_repository: DoctorRepository):
        self.doctor_repository = doctor_repository

    async def __call__(
        self, 
        doctor_id: UUID, 
        name: Optional[str] = None,
        surname: Optional[str] = None,
        age: Optional[int] = None,
        specialization: Optional[str] = None,
        category: Optional[CategoryEnum] = None,
        password: Optional[str] = None
    ) -> Doctor:
        # Проверяем существование врача
        existing_doctor = await self.doctor_repository.get(id=doctor_id)
        if not existing_doctor:
            raise DoctorNotFoundError(doctor_id)
        
        # Подготавливаем данные для обновления
        updates = {}
        if name is not None:
            updates["name"] = name
        if surname is not None:
            updates["surname"] = surname
        if age is not None:
            updates["age"] = age
        if specialization is not None:
            updates["specialization"] = specialization
        if category is not None:
            updates["category"] = category
        if password is not None:
            updates["password"] = get_password_hash(password)
        
        # Обновляем врача
        updated_doctor = await self.doctor_repository.update(str(doctor_id), **updates)
        if not updated_doctor:
            raise DoctorNotFoundError(doctor_id)
        
        return updated_doctor