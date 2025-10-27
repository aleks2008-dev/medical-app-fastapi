from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Room:
    number: int
    uuid: UUID = field(default_factory=uuid4)
    
    @property
    def id(self) -> UUID:
        return self.uuid
    
    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "uuid": str(self.uuid)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Room':
        return cls(
            number=data["number"],
            uuid=UUID(data["uuid"]) if "uuid" in data else uuid4()
        )
    