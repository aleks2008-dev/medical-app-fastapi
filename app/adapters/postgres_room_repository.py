from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any, Optional, List

from app.repository.room_repository import RoomRepository
from app.domain.entities.room import Room
from app.infrastructure.database.models import RoomORM


class DatabaseException(Exception):
    def __str__(self):
        return "Database is not currently available. Please try again later."


class PostgresRoomRepository(RoomRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, **filters: Any) -> Optional[Room]:
        try:
            query = select(RoomORM)
            
            if 'id' in filters:
                query = query.where(RoomORM.id == filters['id'])
            if 'number' in filters:
                query = query.where(RoomORM.number == filters['number'])
            
            result = await self.session.execute(query)
            room_orm = result.scalar_one_or_none()
            
            if room_orm:
                return Room(
                    number=room_orm.number,
                    uuid=room_orm.id
                )
            return None
            
        except Exception:
            raise DatabaseException
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Room]:
        try:
            query = select(RoomORM).offset(skip).limit(limit)
            result = await self.session.execute(query)
            rooms_orm = result.scalars().all()
            
            return [
                Room(
                    number=room_orm.number,
                    uuid=room_orm.id
                )
                for room_orm in rooms_orm
            ]
            
        except Exception:
            raise DatabaseException

    async def add(self, room: Room) -> None:
        try:
            room_db = RoomORM(
                id=room.id,
                number=room.number
            )
            self.session.add(room_db)
            await self.session.commit()
            
        except Exception:
            await self.session.rollback()
            raise DatabaseException
