from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from uuid import UUID

from app.use_cases.crud_appointment import GetAppointment, CreateAppointment, ListAppointments
from app.use_cases.delete_appointment import DeleteAppointment
from app.api.dependencies import (
    get_appointment_use_case,
    create_appointment_use_case,
    list_appointments_use_case,
    delete_appointment_use_case
)
from app.api.auth import get_current_active_user, get_admin_user

from app.api.routers.schema import AppointmentItemCreate, AppointmentItem
from app.domain.entities.user import User, UserRole

router = APIRouter()


@router.get("/appointments/{appointment_id}", response_model=AppointmentItem)
async def get_appointment(
    appointment_id: UUID,
    use_case: GetAppointment = Depends(get_appointment_use_case)
):
    return await use_case(appointment_id)

@router.post("/appointments", response_model=AppointmentItem)
async def create_appointment(
    appointment_data: AppointmentItemCreate,
    use_case: CreateAppointment = Depends(create_appointment_use_case)
):
    return await use_case(appointment_data.to_entity())

@router.get("/appointments", response_model=list[AppointmentItem])
async def list_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    use_case: ListAppointments = Depends(list_appointments_use_case)
):
    return await use_case(skip=skip, limit=limit)

@router.delete("/appointments/{appointment_id}")
async def delete_appointment(
    appointment_id: UUID,
    use_case: DeleteAppointment = Depends(delete_appointment_use_case),
    current_user: User = Depends(get_current_active_user)
):
    await use_case(appointment_id)
    return {"message": "Appointment deleted successfully"}
