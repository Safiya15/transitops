from fastapi import APIRouter

from .schemas import LoginRequest, CreateUserRequest
from .services import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

service = AuthService()


@router.post("/create-user")
async def create_user(data: CreateUserRequest):
    return await service.create_user(data)


@router.post("/login")
async def login(data: LoginRequest):
    return await service.login(data)
