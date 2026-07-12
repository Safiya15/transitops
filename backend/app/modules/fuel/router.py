from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .schemas import CreateFuelLogRequest, FuelLogResponse
from .services import FuelService

router = APIRouter(
    prefix="/fuel",
    tags=["Fuel"]
)

service = FuelService()


@router.post(
    "/",
    response_model=FuelLogResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_fuel_log(
    data: CreateFuelLogRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.create_fuel_log(data)


@router.get(
    "/",
    response_model=List[FuelLogResponse]
)
async def get_all_logs(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER
        )
    )
):
    return await service.get_all_logs()


@router.get(
    "/trip/{trip_id}",
    response_model=FuelLogResponse
)
async def get_trip_log(
    trip_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER
        )
    )
):
    return await service.get_trip_log(trip_id)


@router.get(
    "/vehicle/{vehicle_id}",
    response_model=List[FuelLogResponse]
)
async def get_vehicle_history(
    vehicle_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER
        )
    )
):
    return await service.vehicle_history(vehicle_id)
