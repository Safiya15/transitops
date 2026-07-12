from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .schemas import (
    CreateRoadRequest,
    UpdateRoadRequest,
    RoadResponse
)
from .services import RoadService

router = APIRouter(
    prefix="/roads",
    tags=["Roads"]
)

service = RoadService()


@router.post(
    "/",
    response_model=RoadResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_road(
    data: CreateRoadRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.create_road(data)


@router.get(
    "/",
    response_model=List[RoadResponse]
)
async def get_all_roads(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER
        )
    )
):
    return await service.get_all_roads()


@router.get(
    "/{road_id}",
    response_model=RoadResponse
)
async def get_road(
    road_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER
        )
    )
):
    return await service.get_road(road_id)


@router.put(
    "/{road_id}",
    response_model=RoadResponse
)
async def update_road(
    road_id: str,
    data: UpdateRoadRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.update_road(
        road_id,
        data
    )


@router.patch(
    "/{road_id}/deactivate",
    response_model=RoadResponse
)
async def deactivate_road(
    road_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.deactivate_road(
        road_id
    )
