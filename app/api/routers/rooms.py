from fastapi import APIRouter, Depends

from app.use_cases.crud_room import CreateRoom
from app.api.dependencies import create_room_use_case


from app.api.routers.schema import RoomItemCreate

router = APIRouter()

@router.post("/rooms", response_model=RoomItemCreate)
async def create_room(
    room_data: RoomItemCreate,
    use_case: CreateRoom = Depends(create_room_use_case)
):
    return await use_case(room_data.to_entity())

