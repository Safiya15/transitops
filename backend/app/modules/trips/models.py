from datetime import datetime
from enum import Enum
from typing import List, Optional

# pyrefly: ignore [missing-import]
from beanie import Document, PydanticObjectId
from pydantic import Field


class TripStatus(str, Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Trip(Document):

    vehicle_id: PydanticObjectId

    driver_id: PydanticObjectId

    source_depot_id: PydanticObjectId

    destination_depot_id: PydanticObjectId

    route: List[PydanticObjectId]

    total_distance: float

    estimated_time: float

    cargo_weight: float

    status: TripStatus = TripStatus.SCHEDULED

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        name = "trips"
