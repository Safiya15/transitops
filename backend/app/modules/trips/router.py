from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .schemas import CreateTripRequest, TripResponse
from .services import TripService

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)

service = TripService()


@router.post(
    "/",
    response_model=TripResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_trip(
    data: CreateTripRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DISPATCHER,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.create_trip(data)


@router.get(
    "/",
    response_model=List[TripResponse]
)
async def get_all_trips(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DISPATCHER,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.get_all_trips()


@router.get(
    "/{trip_id}",
    response_model=TripResponse
)
async def get_trip(
    trip_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DISPATCHER,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.get_trip(trip_id)


@router.patch(
    "/{trip_id}/complete",
    response_model=TripResponse
)
async def complete_trip(
    trip_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DISPATCHER,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.complete_trip(trip_id)


@router.patch(
    "/{trip_id}/cancel",
    response_model=TripResponse
)
async def cancel_trip(
    trip_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DISPATCHER,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.cancel_trip(trip_id)
