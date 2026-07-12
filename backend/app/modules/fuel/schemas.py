from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator


class CreateFuelLogRequest(BaseModel):
    trip_id: str
    litres: float = Field(gt=0)
    cost: float = Field(gt=0)


class FuelLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vehicle_id: str
    trip_id: str
    litres: float
    cost: float
    price_per_litre: float
    fuel_efficiency: float
    created_at: datetime

    @field_validator("id", "vehicle_id", "trip_id", mode="before")
    @classmethod
    def stringify_ids(cls, v) -> str:
        return str(v)
