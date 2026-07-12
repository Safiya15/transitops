from fastapi import APIRouter, Depends

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .schemas import (
    FleetSummaryResponse,
    VehicleReportResponse,
    FuelReportResponse,
    ExpenseReportResponse,
    MaintenanceReportResponse
)
from .services import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

service = ReportService()


@router.get(
    "/fleet-summary",
    response_model=FleetSummaryResponse
)
async def fleet_summary(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FINANCIAL_ANALYST,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.fleet_summary()


@router.get(
    "/vehicle/{vehicle_id}",
    response_model=VehicleReportResponse
)
async def vehicle_report(
    vehicle_id: str,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FINANCIAL_ANALYST,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.vehicle_report(vehicle_id)


@router.get(
    "/fuel",
    response_model=FuelReportResponse
)
async def fuel_report(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FINANCIAL_ANALYST,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.fuel_report()


@router.get(
    "/expense",
    response_model=ExpenseReportResponse
)
async def expense_report(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FINANCIAL_ANALYST
        )
    )
):
    return await service.expense_report()


@router.get(
    "/maintenance",
    response_model=MaintenanceReportResponse
)
async def maintenance_report(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER
        )
    )
):
    return await service.maintenance_report()
