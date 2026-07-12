from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .models import TripStatus


class CreateTripRequest(BaseModel):
    vehicle_id: str
    driver_id: str
    source_depot_id: str
    destination_depot_id: str
    cargo_weight: float = Field(gt=0)


class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vehicle_id: str
    driver_id: str
    source_depot_id: str
    destination_depot_id: str
    route: List[str]
    total_distance: float
    estimated_time: float
    cargo_weight: float
    status: TripStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    @field_validator("id", "vehicle_id", "driver_id", "source_depot_id", "destination_depot_id", mode="before")
    @classmethod
    def stringify_ids(cls, v) -> str:
        return str(v)

    @field_validator("route", mode="before")
    @classmethod
    def stringify_route(cls, v) -> List[str]:
        return [str(node) for node in v]
