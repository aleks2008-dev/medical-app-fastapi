from abc import ABC, abstractmethod
from typing import Any, Optional, List
from app.domain.entities.room import Room

class RoomRepository(ABC):
    @abstractmethod
    async def get(self, **filters: Any) -> Optional[Room]:
        pass
    
    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[Room]:
        pass
    
    @abstractmethod
    async def add(self, user: Room) -> None:
        pass
    