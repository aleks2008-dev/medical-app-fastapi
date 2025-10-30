import uuid
from datetime import date as DateType, datetime
from enum import StrEnum

from sqlalchemy import UUID, Boolean, Date, DateTime, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(AsyncAttrs, DeclarativeBase):
    pass

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

class DoctorORM(Base):
    """Doctor database model representing medical professionals."""
    __tablename__ = "doctors"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    surname: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int]
    specialization: Mapped[str]
    category: Mapped[CategoryEnum]
    password: Mapped[str]

    appointments: Mapped[list["AppointmentORM"]] = relationship(back_populates="doctor")


class UserORM(Base):
    """User database model representing system users with authentication."""
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int | None] = mapped_column(nullable=True)
    phone: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    role: Mapped[UserRole] = mapped_column(server_default="user")
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    reset_token: Mapped[str | None] = mapped_column(nullable=True)
    reset_token_expires: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    appointments: Mapped[list["AppointmentORM"]] = relationship(back_populates="user")


class RoomORM(Base):
    """ ORM model representing a room in the database."""
    __tablename__ = "rooms"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    number: Mapped[int]

    appointments: Mapped[list["AppointmentORM"]] = relationship(back_populates="room")


class AppointmentORM(Base):
    """ORM model representing an appointment in the database."""
    __tablename__ = "appointments"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date: Mapped[DateType] = mapped_column(Date)
    doctor_id: Mapped[UUID] = mapped_column(ForeignKey('doctors.id', ondelete="CASCADE"))
    doctor: Mapped["DoctorORM"] = relationship(back_populates="appointments")
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    user: Mapped["UserORM"] = relationship(back_populates="appointments")
    room_id: Mapped[UUID] = mapped_column(ForeignKey('rooms.id', ondelete="CASCADE"))
    room: Mapped["RoomORM"] = relationship(back_populates="appointments")
