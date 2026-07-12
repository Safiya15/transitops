from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .schemas import (
    CreateMaintenanceRequest,
    UpdateMaintenanceRequest,
    MaintenanceResponse
)
from .services import MaintenanceService

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)

service = MaintenanceService()


@router.post(
    "/",
    response_model=MaintenanceResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_maintenance(
    data: CreateMaintenanceRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.create_maintenance(data)


@router.get(
    "/",
    response_model=List[MaintenanceResponse]
)
async def get_all_maintenance(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.get_all_maintenance()


@router.get(
    "/{maintenance_id}",
    response_model=MaintenanceResponse
)
async def get_maintenance(
    maintenance_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.get_maintenance(maintenance_id)


@router.patch(
    "/{maintenance_id}/start",
    response_model=MaintenanceResponse
)
async def start_maintenance(
    maintenance_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.start_maintenance(
        maintenance_id
    )


@router.patch(
    "/{maintenance_id}/complete",
    response_model=MaintenanceResponse
)
async def complete_maintenance(
    maintenance_id: str,
    data: UpdateMaintenanceRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.complete_maintenance(
        maintenance_id,
        data.cost
    )
