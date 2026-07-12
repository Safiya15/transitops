from datetime import datetime
from enum import Enum
from typing import Optional

# pyrefly: ignore [missing-import]
from beanie import Document, PydanticObjectId
from pydantic import Field


class MaintenanceStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class MaintenanceType(str, Enum):
    SCHEDULED = "Scheduled"
    BREAKDOWN = "Breakdown"
    PREVENTIVE = "Preventive"


class Maintenance(Document):

    vehicle_id: PydanticObjectId

    maintenance_type: MaintenanceType

    description: str

    cost: float = 0

    service_due_at: float

    status: MaintenanceStatus = MaintenanceStatus.PENDING

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "maintenance"
