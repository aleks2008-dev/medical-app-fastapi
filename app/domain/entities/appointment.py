from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Appointment:
    datetime: datetime
    doctor_id: UUID
    user_id: UUID
    room_id: UUID
    uuid: UUID = field(default_factory=uuid4)
    
    @property
    def id(self) -> UUID:
        return self.uuid
    
    def to_dict(self) -> dict:
        return {
            "datetime": self.datetime,
            "doctor_id": str(self.doctor_id),
            "user_id": str(self.user_id),
            "room_id": str(self.room_id),
            "uuid": str(self.uuid)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Appointment':
        return cls(
            datetime=data["datetime"],
            doctor_id=UUID(data["doctor_id"]),
            user_id=UUID(data["user_id"]),
            room_id=UUID(data["room_id"]),
            uuid=UUID(data["uuid"]) if "uuid" in data else uuid4()
        )
 