from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.room_repository import RoomRepository
from app.domain.entities.room import Room
from app.infrastructure.database.models import RoomORM


class DatabaseException(Exception):
    def __str__(self):
        return "Database is not currently available. Please try again later."


class PostgresRoomRepository(RoomRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

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
