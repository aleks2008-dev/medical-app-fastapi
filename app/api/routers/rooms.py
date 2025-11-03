from fastapi import APIRouter, Depends, Query
from typing import List

from app.use_cases.crud_room import CreateRoom, ListRooms
from app.api.dependencies import create_room_use_case, list_rooms_use_case

from app.api.routers.schema import RoomItemCreate, RoomItem

router = APIRouter()

@router.post("/rooms", response_model=RoomItemCreate)
async def create_room(
    room_data: RoomItemCreate,
    use_case: CreateRoom = Depends(create_room_use_case)
):
    return await use_case(room_data.to_entity())

@router.get("/rooms", response_model=List[RoomItem])
async def list_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    use_case: ListRooms = Depends(list_rooms_use_case)
):
    return await use_case(skip=skip, limit=limit)

