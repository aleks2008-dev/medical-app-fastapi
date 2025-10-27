from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.use_cases.auth import AuthService
from app.api.auth import get_user_repository
from app.api.routers.schema import (
    UserItemCreate, 
    TokenData, 
    RefreshTokenRequest, 
    PasswordResetRequest, 
    PasswordResetConfirm,
    UserPublic
)
from app.api.auth import get_current_active_user
from app.domain.entities.user import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter()

async def get_auth_service(user_repository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)

@router.post("/register", response_model=UserPublic)
async def register(
    user_data: UserItemCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.register_user(
        name=user_data.name,
        surname=user_data.surname,
        email=user_data.email,
        password=user_data.password,
        phone=user_data.phone
    )
    return UserPublic(
        id=user.id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        age=user.age,
        phone=user.phone,
        role=user.role,
        disabled=user.disabled
    )

@router.post("/login", response_model=TokenData)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    tokens = await auth_service.create_tokens(user)
    return TokenData(**tokens)

@router.post("/refresh", response_model=TokenData)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    tokens = await auth_service.refresh_access_token(refresh_data.refresh_token)
    return TokenData(**tokens)

@router.post("/password-reset-request")
async def request_password_reset(
    reset_request: PasswordResetRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.request_password_reset(reset_request.email)

@router.post("/password-reset-confirm")
async def confirm_password_reset(
    reset_confirm: PasswordResetConfirm,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.reset_password(reset_confirm.token, reset_confirm.new_password)

@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.logout_user(str(current_user.id), credentials.credentials)