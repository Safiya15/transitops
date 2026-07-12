from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .services import DepotService
from .schemas import (
    CreateDepotRequest,
    UpdateDepotRequest,
    DepotResponse
)

router = APIRouter(
    prefix="/depots",
    tags=["Depots"]
)

service = DepotService()


@router.post(
    "/",
    response_model=DepotResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_depot(
    data: CreateDepotRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.create_depot(data)


@router.get(
    "/",
    response_model=List[DepotResponse]
)
async def get_all_depots(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER
        )
    )
):
    return await service.get_all_depots()


@router.get(
    "/{depot_id}",
    response_model=DepotResponse
)
async def get_depot(
    depot_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER
        )
    )
):
    return await service.get_depot(depot_id)


@router.put(
    "/{depot_id}",
    response_model=DepotResponse
)
async def update_depot(
    depot_id: str,
    data: UpdateDepotRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.update_depot(
        depot_id,
        data
    )


@router.patch(
    "/{depot_id}/deactivate",
    response_model=DepotResponse
)
async def deactivate_depot(
    depot_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.deactivate_depot(
        depot_id
    )
