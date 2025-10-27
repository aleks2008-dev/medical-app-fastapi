from typing import Any, Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repository.doctor_repository import DoctorRepository
from app.domain.entities.doctor import Doctor
from app.infrastructure.database.models import DoctorORM


class DatabaseException(Exception):
    def __str__(self):
        return "Database is not currently available. Please try again later."


class PostgresDoctorRepository(DoctorRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, **filters: Any) -> Optional[Doctor]:
        try:
            query = select(DoctorORM)
            
            if doctor_id := filters.get('id'):
                query = query.where(DoctorORM.id == doctor_id)
            
            result = await self.session.execute(query)
            doctor_db = result.scalar_one_or_none()
            
            return self._to_entity(doctor_db) if doctor_db else None
            
        except Exception as e:
            print(f'PostgreSQL get error: {e}')
            raise DatabaseException

    async def add(self, doctor: Doctor) -> None:
        try:
            doctor_db = DoctorORM(
                id=doctor.id,
                name=doctor.name,
                surname=doctor.surname,
                age=doctor.age,
                specialization=doctor.specialization,
                category=doctor.category,
                password=doctor.password
            )
            self.session.add(doctor_db)
            await self.session.commit()
            
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException

    async def update(self, doctor_id: str, **updates: Any) -> Optional[Doctor]:
        try:
            query = select(DoctorORM).where(DoctorORM.id == UUID(doctor_id))
            result = await self.session.execute(query)
            doctor_db = result.scalar_one_or_none()
            
            if not doctor_db:
                return None
            
            for key, value in updates.items():
                if value is not None and hasattr(doctor_db, key):
                    setattr(doctor_db, key, value)
            
            await self.session.commit()
            return self._to_entity(doctor_db)
            
        except Exception as e:
            await self.session.rollback()
            print(f'PostgreSQL update error: {e}')
            raise DatabaseException

    async def delete(self, doctor_id: str) -> bool:
        try:
            query = select(DoctorORM).where(DoctorORM.id == UUID(doctor_id))
            result = await self.session.execute(query)
            doctor_db = result.scalar_one_or_none()
            
            if doctor_db:
                await self.session.delete(doctor_db)
                await self.session.commit()
                return True
            return False
            
        except Exception as e:
            await self.session.rollback()
            print(f'PostgreSQL delete error: {e}')
            raise DatabaseException

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Doctor]:
        try:
            query = select(DoctorORM).offset(skip).limit(limit)
            result = await self.session.execute(query)
            doctors_db = result.scalars().all()
            
            return [self._to_entity(doctor_db) for doctor_db in doctors_db]
            
        except Exception as e:
            print(f'PostgreSQL list_all error: {e}')
            raise DatabaseException

    def _to_entity(self, doctor_db: DoctorORM) -> Doctor:
        return Doctor(
            name=doctor_db.name,
            surname=doctor_db.surname,
            age=doctor_db.age,
            specialization=doctor_db.specialization,
            category=doctor_db.category,
            password=doctor_db.password,
            uuid=doctor_db.id
        )
    
    