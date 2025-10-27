import re
from datetime import date
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StrictInt,
    StrictStr,
    computed_field,
    field_validator
)
from uuid import UUID
from enum import StrEnum

class CategoryEnum(StrEnum):
    """Medical doctor qualification categories"""
    FIRST = "first"
    SECOND = "second"
    HIGHEST = "highest"
    NO_CATEGORY = "no_category"


class UserRole(StrEnum):
    """User roles in the healthcare system"""
    user = "user"
    admin = "admin"
    doctor = "doctor"


class DoctorItemCreate(BaseModel):
    name: StrictStr = Field(min_length=3, max_length=10)
    surname: StrictStr = Field(min_length=3, max_length=10)
    age: StrictInt = Field(ge=0)
    specialization: StrictStr = Field(min_length=3)
    category: CategoryEnum
    password: str = Field(exclude=True, min_length=4)

    @field_validator('age')
    def check_age(cls, value):
        if value < 0:
            raise ValueError('Age cannot be negative')
        return value

    @computed_field
    def full_name(self) -> str:
        return f"{self.name} {self.surname}"
    
    def to_entity(self):
        from app.domain.entities.doctor import Doctor
        return Doctor(
            name=self.name,
            surname=self.surname,
            age=self.age,
            specialization=self.specialization,
            category=self.category,
            password=self.password
        )


class DoctorResponse(BaseModel):
    id: UUID
    name: StrictStr
    surname: StrictStr
    age: StrictInt
    specialization: StrictStr
    category: CategoryEnum


class DoctorItemUpdate(BaseModel):
    """For updating doctor records with optional fields."""
    name: StrictStr | None = Field(default=None, min_length=3, max_length=10)
    surname: StrictStr | None = Field(default=None, min_length=3, max_length=10)
    age: StrictInt | None = Field(default=None, ge=0)
    specialization: StrictStr | None = Field(default=None, min_length=3)
    category: CategoryEnum | None = None
    password: str | None = Field(default=None, min_length=5, exclude=True)


class BaseUser(BaseModel):
    name: StrictStr | None = Field(default=None, min_length=3, max_length=10)
    surname: StrictStr | None = Field(default=None, min_length=3, max_length=10)
    email: EmailStr
    age: StrictInt | None = Field(default=None, ge=0)
    phone: str | None = None

    @field_validator('phone')
    def validate_phone_number(cls, value: str | None):
        pattern = r"""
                ^(\+375|80)?          # Код страны/оператора
                [\s\-\(\)]*          # Допустимые разделители
                (\d{2})               # Первые 2 цифры
                [\s\-\(\)]*           # Разделители
                (\d{3})              # Следующие 3 цифры
                [\s\-\(\)]*           # Разделители
                (\d{2})              # Предпоследние 2 цифры
                [\s\-\(\)]*           # Разделители
                (\d{2})$             # Последние 2 цифры
            """
        if value is None:
            return None
        if not re.fullmatch(pattern, value, flags=re.VERBOSE):
            raise ValueError("Invalid phone number format")
        cleaned_value = re.sub(r'\D', '', value)
        if not (7 <= len(cleaned_value) <= 15):
            raise ValueError('Phone number must be between 7 and 15 digits.')
        return value


class UserItemCreate(BaseUser):
    password: str = Field(exclude=True, min_length=8)
    role: UserRole | None = None
    
    def to_entity(self):
        from app.domain.entities.user import User
        return User(
            name=self.name,
            surname=self.surname,
            email=self.email,
            age=self.age,
            phone=self.phone,
            role=self.role or UserRole.user,
            hashed_password=self.password  # В реальном приложении нужно хешировать
        )


class UserItem(BaseUser):
    id: UUID
    role: UserRole | None = None


class UserItemUpdate(BaseModel):
    name: StrictStr | None = Field(default=None, min_length=3, max_length=10)
    surname: StrictStr | None = Field(default=None, min_length=3, max_length=10)
    email: EmailStr | None = None
    age: StrictInt | None = Field(default=None, ge=0)
    phone: str | None = None
    password: str | None = Field(default=None, min_length=8)
    role: UserRole | None = None
    disabled: bool | None = None


class UserPublic(BaseModel):
    id: UUID
    name: str
    surname: str
    email: str
    age: StrictInt | None = None
    phone: str | None = None
    role: UserRole
    disabled: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class CurrentUser(UserPublic):
    access_token: Optional[str] = None
    token_type: Optional[str] = "bearer"

class RoomItemCreate(BaseModel):
    number: StrictInt | None = Field(default=None, ge=0, le=100)


class RoomItem(RoomItemCreate):
    id: UUID


class AppointmentItemCreate(BaseModel):
    date: date
    doctor_id: UUID
    user_id: UUID
    room_id: UUID

    @field_validator('date', mode='before')
    def parse_date(cls, value):
        if isinstance(value, int):
            # Convert from YYYYMMDD format to date
            return date(
                year=value // 10000,
                month=(value % 10000) // 100,
                day=value % 100
            )
        return value
    
    def to_entity(self):
        from app.domain.entities.appointment import Appointment
        return Appointment(
            date=self.date,
            doctor_id=self.doctor_id,
            user_id=self.user_id,
            room_id=self.room_id
        )


class AppointmentItem(AppointmentItemCreate):
    id: UUID


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str