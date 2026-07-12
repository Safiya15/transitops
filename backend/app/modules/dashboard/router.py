from fastapi import APIRouter, Depends

from app.core.dependencies import require_roles
from app.modules.users.models import UserRole

from .services import DashboardService
from .schemas import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

service = DashboardService()


@router.get(
    "/",
    response_model=DashboardResponse
)
async def get_dashboard(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.FLEET_MANAGER,
            UserRole.FINANCIAL_ANALYST
        )
    )
):
    return await service.get_dashboard()
