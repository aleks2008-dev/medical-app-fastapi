from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from uuid import UUID
from app.domain.entities.user import User, UserRole

from app.use_cases.crud_user import GetUser, CreateUser, ListUsers
from app.use_cases.update_user import UpdateUser
from app.use_cases.delete_user import DeleteUser
from app.api.dependencies import (
    get_user_use_case,
    create_user_use_case,
    list_users_use_case,
    update_user_use_case,
    delete_user_use_case
)

from app.api.routers.schema import UserItemCreate, UserItem, UserItemUpdate
from app.api.auth import get_current_active_user, get_admin_user

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserItem)
async def get_user(
    user_id: UUID,
    use_case: GetUser = Depends(get_user_use_case)
):
    return await use_case(user_id)

@router.post("/users", response_model=UserItem)
async def create_user(
    user_data: UserItemCreate,
    use_case: CreateUser = Depends(create_user_use_case)
):
    return await use_case(user_data.to_entity())

@router.get("/users", response_model=list[UserItem])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    use_case: ListUsers = Depends(list_users_use_case),
    current_user: User = Depends(get_admin_user)
):
    return await use_case(skip=skip, limit=limit)

@router.patch("/users/{user_id}", response_model=UserItem)
async def update_user(
    user_id: UUID,
    user_data: UserItemUpdate,
    use_case: UpdateUser = Depends(update_user_use_case),
    current_user: User = Depends(get_current_active_user)
):
    # Обычные пользователи могут редактировать только себя
    # Админы могут редактировать всех
    if current_user.role != UserRole.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Обычные пользователи не могут менять роль
    if current_user.role != UserRole.admin and user_data.role is not None:
        user_data.role = None
    
    return await use_case(
        user_id=user_id,
        name=user_data.name,
        surname=user_data.surname,
        email=user_data.email,
        age=user_data.age,
        phone=user_data.phone,
        role=user_data.role,
        password=user_data.password,
        disabled=user_data.disabled
    )

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: UUID,
    use_case: DeleteUser = Depends(delete_user_use_case),
    current_user: User = Depends(get_current_active_user)
):
    # Обычные пользователи могут удалять только себя
    # Администраторы могут удалять всех
    if current_user.role != UserRole.admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    await use_case(user_id)
    return {"message": "User deleted successfully"}
