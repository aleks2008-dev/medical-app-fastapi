from uuid import UUID, uuid4
from dataclasses import dataclass, field
from enum import StrEnum
from datetime import datetime

class UserRole(StrEnum):
    user = "user"
    admin = "admin"
    doctor = "doctor"

@dataclass
class User:
    name: str
    surname: str
    email: str
    hashed_password: str
    age: int | None = None
    phone: str | None = None
    role: UserRole = UserRole.user
    disabled: bool = False
    reset_token: str | None = None
    reset_token_expires: datetime | None = None
    uuid: UUID = field(default_factory=uuid4)
    
    @property
    def id(self) -> UUID:
        return self.uuid
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "age": self.age,
            "phone": self.phone,
            "role": self.role.value,
            "disabled": self.disabled,
            "hashed_password": self.hashed_password,
            "reset_token": self.reset_token,
            "reset_token_expires": self.reset_token_expires.isoformat() if self.reset_token_expires else None,
            "uuid": str(self.uuid)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        reset_token_expires = None
        if data.get("reset_token_expires"):
            reset_token_expires = datetime.fromisoformat(data["reset_token_expires"])
        
        return cls(
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            age=data.get("age"),
            phone=data.get("phone"),
            role=UserRole(data.get("role", "user")),
            disabled=data.get("disabled", False),
            hashed_password=data["hashed_password"],
            reset_token=data.get("reset_token"),
            reset_token_expires=reset_token_expires,
            uuid=UUID(data["uuid"]) if "uuid" in data else uuid4()
        )
    
