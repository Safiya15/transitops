from typing import List

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_active_user, require_roles
from app.modules.auth.schemas import CreateUserRequest
from app.modules.users.models import UserRole
from app.modules.users.schemas import (
    UpdateUserRoleRequest,
    UpdateUserStatusRequest,
    UserResponse,
)
from app.modules.users.services import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

user_service = UserService()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def create_user(
    user_data: CreateUserRequest,
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    return await user_service.create_user(user_data)


@router.get(
    "/",
    response_model=List[UserResponse],
)
async def get_all_users(
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    return await user_service.get_all_users()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: str,
    current_user=Depends(get_current_active_user),
):
    return await user_service.get_user(user_id)


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
)
async def update_user_role(
    user_id: str,
    role_data: UpdateUserRoleRequest,
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    return await user_service.update_role(user_id, role_data.role)


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
)
async def update_user_status(
    user_id: str,
    status_data: UpdateUserStatusRequest,
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    return await user_service.update_status(user_id, status_data.is_active)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: str,
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    await user_service.delete_user(user_id)
