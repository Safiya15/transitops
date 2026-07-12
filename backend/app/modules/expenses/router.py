from typing import List
from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .schemas import CreateExpenseRequest, ExpenseResponse
from .services import ExpenseService

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

service = ExpenseService()


@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_expense(
    data: CreateExpenseRequest,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.SAFETY_OFFICER,
            UserRole.FINANCIAL_ANALYST
        )
    )
):
    return await service.create_expense(data)


@router.get(
    "/",
    response_model=List[ExpenseResponse]
)
async def get_all_expenses(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.FINANCIAL_ANALYST
        )
    )
):
    return await service.get_all_expenses()


@router.get(
    "/trip/{trip_id}",
    response_model=List[ExpenseResponse]
)
async def get_trip_expenses(
    trip_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER,
            UserRole.FINANCIAL_ANALYST
        )
    )
):
    return await service.trip_expenses(trip_id)


@router.get(
    "/vehicle/{vehicle_id}",
    response_model=List[ExpenseResponse]
)
async def get_vehicle_expenses(
    vehicle_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.DISPATCHER,
            UserRole.FINANCIAL_ANALYST
        )
    )
):
    return await service.vehicle_expenses(vehicle_id)
