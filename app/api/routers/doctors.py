from fastapi import APIRouter, Depends,  Query
from uuid import UUID

from app.use_cases.crud_doctor import GetDoctor, CreateDoctor, ListDoctors
from app.use_cases.update_doctor import UpdateDoctor
from app.use_cases.delete_doctor import DeleteDoctor
from app.api.dependencies import (
    get_doctor_use_case,
    create_doctor_use_case,
    list_doctors_use_case,
    update_doctor_use_case,
    delete_doctor_use_case
)
from app.api.auth import get_current_active_user, get_admin_user
from app.domain.entities.user import User
from app.api.routers.schema import DoctorItemCreate, DoctorResponse, DoctorItemUpdate

router = APIRouter()


@router.get("/doctors/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(
    doctor_id: UUID,
    use_case: GetDoctor = Depends(get_doctor_use_case)
):
    return await use_case(doctor_id)

@router.post("/doctors", response_model=DoctorResponse)
async def create_doctor(
    doctor_data: DoctorItemCreate,
    use_case: CreateDoctor = Depends(create_doctor_use_case),
    current_user: User = Depends(get_admin_user)
):
    return await use_case(doctor_data.to_entity())

@router.get("/doctors", response_model=list[DoctorResponse])
async def list_doctors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    use_case: ListDoctors = Depends(list_doctors_use_case),
    current_user: User = Depends(get_current_active_user)
):
    return await use_case(skip=skip, limit=limit)

@router.patch("/doctors/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(
    doctor_id: UUID,
    doctor_data: DoctorItemUpdate,
    use_case: UpdateDoctor = Depends(update_doctor_use_case),
    current_user: User = Depends(get_admin_user)
):
    return await use_case(
        doctor_id=doctor_id,
        name=doctor_data.name,
        surname=doctor_data.surname,
        age=doctor_data.age,
        specialization=doctor_data.specialization,
        category=doctor_data.category,
        password=doctor_data.password
    )

@router.delete("/doctors/{doctor_id}")
async def delete_doctor(
    doctor_id: UUID,
    use_case: DeleteDoctor = Depends(delete_doctor_use_case),
    current_user: User = Depends(get_admin_user)
):
    await use_case(doctor_id)
    return {"message": "Doctor deleted successfully"}
