from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.postgres_user_repository import PostgresUserRepository
from app.adapters.postgres_appointment_repository import PostgresAppointmentRepository
from app.adapters.postgres_doctor_repository import PostgresDoctorRepository
from app.adapters.postgres_room_repository import PostgresRoomRepository
from app.adapters.password_hasher import SHA256PasswordHasher
from app.repository.doctor_repository import DoctorRepository
from app.repository.user_repository import UserRepository
from app.repository.appointment_repository import AppointmentRepository
from app.repository.room_repository import RoomRepository
from app.use_cases.crud_doctor import GetDoctor, CreateDoctor, ListDoctors
from app.use_cases.crud_user import GetUser, CreateUser, ListUsers
from app.use_cases.crud_appointment import GetAppointment, CreateAppointment, ListAppointments
from app.use_cases.update_doctor import UpdateDoctor
from app.use_cases.update_user import UpdateUser
from app.use_cases.delete_doctor import DeleteDoctor
from app.use_cases.delete_user import DeleteUser
from app.use_cases.delete_appointment import DeleteAppointment
from app.use_cases.crud_room import CreateRoom
from app.infrastructure.database.postgres import get_db

async def get_doctor_repository(
    session: AsyncSession = Depends(get_db)
) -> DoctorRepository:
    return PostgresDoctorRepository(session)

async def get_doctor_use_case(
    repository: DoctorRepository = Depends(get_doctor_repository)
) -> GetDoctor:
    return GetDoctor(repository)

async def create_doctor_use_case(
    repository: DoctorRepository = Depends(get_doctor_repository)
) -> CreateDoctor:
    return CreateDoctor(repository)

async def list_doctors_use_case(
    repository: DoctorRepository = Depends(get_doctor_repository)
) -> ListDoctors:
    return ListDoctors(repository)

async def update_doctor_use_case(
    repository: DoctorRepository = Depends(get_doctor_repository)
) -> UpdateDoctor:
    return UpdateDoctor(repository)


async def get_user_repository(
    session: AsyncSession = Depends(get_db)
) -> UserRepository:
    return PostgresUserRepository(session)

async def get_user_use_case(
    repository: UserRepository = Depends(get_user_repository)
) -> GetUser:
    return GetUser(repository)

async def create_user_use_case(
    repository: UserRepository = Depends(get_user_repository)
) -> CreateUser:
    return CreateUser(repository, SHA256PasswordHasher())

async def list_users_use_case(
    repository: UserRepository = Depends(get_user_repository)
) -> ListUsers:
    return ListUsers(repository)

async def update_user_use_case(
    repository: UserRepository = Depends(get_user_repository)
) -> UpdateUser:
    return UpdateUser(repository)

async def delete_doctor_use_case(
    repository: DoctorRepository = Depends(get_doctor_repository)
) -> DeleteDoctor:
    return DeleteDoctor(repository)

async def delete_user_use_case(
    repository: UserRepository = Depends(get_user_repository)
) -> DeleteUser:
    return DeleteUser(repository)

async def get_appointment_repository(
    session: AsyncSession = Depends(get_db)
) -> AppointmentRepository:
    return PostgresAppointmentRepository(session)

async def delete_appointment_use_case(
    repository: AppointmentRepository = Depends(get_appointment_repository)
) -> DeleteAppointment:
    return DeleteAppointment(repository)

async def get_appointment_use_case(
    repository: AppointmentRepository = Depends(get_appointment_repository)
) -> GetAppointment:
    return GetAppointment(repository)

async def create_appointment_use_case(
    repository: AppointmentRepository = Depends(get_appointment_repository)
) -> CreateAppointment:
    return CreateAppointment(repository)

async def list_appointments_use_case(
    repository: AppointmentRepository = Depends(get_appointment_repository)
) -> ListAppointments:
    return ListAppointments(repository)


async def get_room_repository(
    session: AsyncSession = Depends(get_db)
) -> RoomRepository:
    return PostgresRoomRepository(session)

async def create_room_use_case(
    repository: RoomRepository = Depends(get_room_repository)
) -> CreateRoom:
    return CreateRoom(repository)