from abc import ABC, abstractmethod
from typing import Any, Optional
from app.domain.entities.appointment import Appointment

class AppointmentRepository(ABC):
    @abstractmethod
    async def get(self, **filters: Any) -> Optional[Appointment]:
        pass
    
    @abstractmethod
    async def add(self, appointment: Appointment) -> None:
        pass
    
    @abstractmethod
    async def update(self, appointment_id: str, **updates: Any) -> Optional[Appointment]:
        pass
    
    @abstractmethod
    async def delete(self, appointment_id: str) -> bool:
        pass
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Appointment]:
        pass
    