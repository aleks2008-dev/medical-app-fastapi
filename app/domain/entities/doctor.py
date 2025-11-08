from uuid import UUID, uuid4
from dataclasses import dataclass, field
from enum import StrEnum

class CategoryEnum(StrEnum):
    FIRST = "first"
    SECOND = "second"
    HIGHEST = "highest"
    NO_CATEGORY = "no_category"

@dataclass
class Doctor:
    name: str
    surname: str
    age: int
    specialization: str
    category: CategoryEnum
    password: str
    experience_years: int = 0
    uuid: UUID = field(default_factory=uuid4)
    
    @property
    def id(self) -> UUID:
        return self.uuid
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "specialization": self.specialization,
            "category": self.category.value,
            "password": self.password,
            "experience_years": self.experience_years,
            "uuid": str(self.uuid)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Doctor':
        return cls(
            name=data["name"],
            surname=data["surname"],
            age=data["age"],
            specialization=data["specialization"],
            category=CategoryEnum(data["category"]),
            password=data["password"],
            experience_years=data.get("experience_years", 0),
            uuid=UUID(data["uuid"]) if "uuid" in data else uuid4()
        )
    
