from typing import List

from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .schemas import CreateVehicleRequest, UpdateVehicleRequest, VehicleResponse
from .services import VehicleService

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
)

service = VehicleService()


@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_vehicle(
    data: CreateVehicleRequest,
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.FLEET_MANAGER)),
):
    return await service.create_vehicle(data)


@router.get(
    "/",
    response_model=List[VehicleResponse],
)
async def get_all_vehicles(
    current_user=Depends(
        require_roles(UserRole.ADMIN, UserRole.FLEET_MANAGER, UserRole.DISPATCHER)
    ),
):
    return await service.get_all_vehicles()


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
async def get_vehicle(
    vehicle_id: str,
    current_user=Depends(
        require_roles(UserRole.ADMIN, UserRole.FLEET_MANAGER, UserRole.DISPATCHER)
    ),
):
    return await service.get_vehicle(vehicle_id)


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
async def update_vehicle(
    vehicle_id: str,
    data: UpdateVehicleRequest,
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.FLEET_MANAGER)),
):
    return await service.update_vehicle(vehicle_id, data)


@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_vehicle(
    vehicle_id: str,
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    await service.delete_vehicle(vehicle_id)
