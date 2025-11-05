from typing import Any, Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repository.appointment_repository import AppointmentRepository
from app.domain.entities.appointment import Appointment
from app.infrastructure.database.models import AppointmentORM


class DatabaseException(Exception):
    def __str__(self):
        return "Database is not currently available. Please try again later."


class PostgresAppointmentRepository(AppointmentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, **filters: Any) -> Optional[Appointment]:
        try:
            query = select(AppointmentORM)
            
            if appointment_id := filters.get('id'):
                query = query.where(AppointmentORM.id == appointment_id)
            
            result = await self.session.execute(query)
            appointment_db = result.scalar_one_or_none()
            
            return self._to_entity(appointment_db) if appointment_db else None
            
        except Exception as e:
            print(f'PostgreSQL get error: {e}')
            raise DatabaseException

    async def add(self, appointment: Appointment) -> None:
        try:
            appointment_db = AppointmentORM(
                id=appointment.id,
                datetime=appointment.datetime,
                doctor_id=appointment.doctor_id,
                user_id=appointment.user_id,
                room_id=appointment.room_id
            )
            self.session.add(appointment_db)
            await self.session.commit()
            
        except Exception:
            await self.session.rollback()
            raise DatabaseException

    async def update(self, appointment_id: str, **updates: Any) -> Optional[Appointment]:
        try:
            query = select(AppointmentORM).where(AppointmentORM.id == UUID(appointment_id))
            result = await self.session.execute(query)
            appointment_db = result.scalar_one_or_none()
            
            if not appointment_db:
                return None
            
            for key, value in updates.items():
                if value is not None and hasattr(appointment_db, key):
                    setattr(appointment_db, key, value)
            
            await self.session.commit()
            return self._to_entity(appointment_db)
            
        except Exception as e:
            await self.session.rollback()
            print(f'PostgreSQL update error: {e}')
            raise DatabaseException

    async def delete(self, appointment_id: str) -> bool:
        try:
            query = select(AppointmentORM).where(AppointmentORM.id == UUID(appointment_id))
            result = await self.session.execute(query)
            appointment_db = result.scalar_one_or_none()
            
            if appointment_db:
                await self.session.delete(appointment_db)
                await self.session.commit()
                return True
            return False
            
        except Exception as e:
            await self.session.rollback()
            print(f'PostgreSQL delete error: {e}')
            raise DatabaseException

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Appointment]:
        try:
            query = select(AppointmentORM).offset(skip).limit(limit)
            result = await self.session.execute(query)
            appointments_db = result.scalars().all()
            
            return [self._to_entity(appointment_db) for appointment_db in appointments_db]
            
        except Exception as e:
            print(f'PostgreSQL list_all error: {e}')
            raise DatabaseException

    def _to_entity(self, appointment_db: AppointmentORM) -> Appointment:
        return Appointment(
            datetime=appointment_db.datetime,
            doctor_id=appointment_db.doctor_id,
            user_id=appointment_db.user_id,
            room_id=appointment_db.room_id,
            uuid=appointment_db.id
        )
    
    