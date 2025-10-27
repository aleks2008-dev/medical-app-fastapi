from uuid import UUID, uuid4
from typing import Optional
from app.domain.entities.doctor import Doctor, CategoryEnum

def create_doctor(
    name: Optional[str] = None,
    surname: Optional[str] = None,
    age: int = 30,
    specialization: Optional[str] = None,
    category: CategoryEnum = CategoryEnum.FIRST,
    password: str = "password123",
    id: Optional[UUID] = None,
) -> Doctor:
    return Doctor(
        name=name or "John",
        surname=surname or "Doe", 
        age=age,
        specialization=specialization or "General Practitioner",
        category=category,
        password=password,
        uuid=id or uuid4()
    )
