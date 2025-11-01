from app.domain.entities.room import Room
from app.repository.room_repository import RoomRepository


class CreateRoom:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    async def __call__(self, room: Room) -> Room:
        await self.room_repository.add(room)  # This is equivalent to await MongoDoctorRepository().add(doctor)
        return room
