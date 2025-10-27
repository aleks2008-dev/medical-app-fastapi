from abc import ABC, abstractmethod
from typing import Any, Optional
from app.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    async def get(self, **filters: Any) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def add(self, user: User) -> None:
        pass
    
    @abstractmethod
    async def update(self, user_id: str, **updates: Any) -> Optional[User]:
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass
    
    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        pass
   