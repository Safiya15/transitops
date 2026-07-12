from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

from .models import MaintenanceStatus, MaintenanceType


class CreateMaintenanceRequest(BaseModel):
    vehicle_id: str
    maintenance_type: MaintenanceType
    description: str
    service_due_at: float


class UpdateMaintenanceRequest(BaseModel):
    description: str
    cost: float


class MaintenanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vehicle_id: str
    maintenance_type: MaintenanceType
    description: str
    cost: float
    service_due_at: float
    status: MaintenanceStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    @field_validator("id", "vehicle_id", mode="before")
    @classmethod
    def stringify_ids(cls, v) -> str:
        return str(v)
