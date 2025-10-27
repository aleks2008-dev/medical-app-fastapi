from abc import ABC, abstractmethod
from typing import Any, Optional
from app.domain.entities.doctor import Doctor

class DoctorRepository(ABC):
    @abstractmethod
    async def get(self, **filters: Any) -> Optional[Doctor]:
        pass
    
    @abstractmethod
    async def add(self, doctor: Doctor) -> None:
        pass
    
    @abstractmethod
    async def update(self, doctor_id: str, **updates: Any) -> Optional[Doctor]:
        pass
    
    @abstractmethod
    async def delete(self, doctor_id: str) -> bool:
        pass
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Doctor]:
        pass
    