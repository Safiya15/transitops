from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class CreateDepotRequest(BaseModel):
    name: str
    city: str
    state: str
    address: str
    latitude: float
    longitude: float


class UpdateDepotRequest(BaseModel):
    name: str
    city: str
    state: str
    address: str
    latitude: float
    longitude: float
    is_active: bool = True


class DepotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    city: str
    state: str
    address: str
    latitude: float
    longitude: float
    is_active: bool
    created_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def stringify_id(cls, v) -> str:
        return str(v)
