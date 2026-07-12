from typing import List

from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .schemas import CreateDriverRequest, UpdateDriverRequest, DriverResponse
from .services import DriverService

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)

driver_service = DriverService()


@router.post(
    "/",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_driver(
    data: CreateDriverRequest,
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.SAFETY_OFFICER)),
):
    return await driver_service.create_driver(data)


@router.get(
    "/",
    response_model=List[DriverResponse],
)
async def get_all_drivers(
    current_user=Depends(
        require_roles(UserRole.ADMIN, UserRole.DISPATCHER, UserRole.SAFETY_OFFICER)
    ),
):
    return await driver_service.get_all_drivers()


@router.get(
    "/{driver_id}",
    response_model=DriverResponse,
)
async def get_driver(
    driver_id: str,
    current_user=Depends(
        require_roles(UserRole.ADMIN, UserRole.DISPATCHER, UserRole.SAFETY_OFFICER)
    ),
):
    return await driver_service.get_driver(driver_id)


@router.put(
    "/{driver_id}",
    response_model=DriverResponse,
)
async def update_driver(
    driver_id: str,
    data: UpdateDriverRequest,
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.SAFETY_OFFICER)),
):
    return await driver_service.update_driver(driver_id, data)


@router.delete(
    "/{driver_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_driver(
    driver_id: str,
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.SAFETY_OFFICER)),
):
    await driver_service.delete_driver(driver_id)
