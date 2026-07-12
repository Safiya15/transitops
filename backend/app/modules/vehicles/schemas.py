from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from .models import VehicleStatus, VehicleType


class CreateVehicleRequest(BaseModel):
    registration_number: str
    manufacturer: str
    model: str
    vehicle_type: VehicleType
    capacity: float
    purchase_cost: float


class UpdateVehicleRequest(BaseModel):
    manufacturer: str
    model: str
    vehicle_type: VehicleType
    capacity: float
    purchase_cost: float


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    registration_number: str
    manufacturer: str
    model: str
    vehicle_type: VehicleType
    capacity: float
    odometer: float
    purchase_cost: float
    status: VehicleStatus
    created_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def stringify_id(cls, v) -> str:
        return str(v)
