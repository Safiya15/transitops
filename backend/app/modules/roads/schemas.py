from pydantic import BaseModel, Field, ConfigDict, field_validator


class CreateRoadRequest(BaseModel):
    source_depot_id: str
    destination_depot_id: str
    distance: float = Field(gt=0)
    average_time: float = Field(gt=0)


class UpdateRoadRequest(BaseModel):
    distance: float = Field(gt=0)
    average_time: float = Field(gt=0)


class RoadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_depot_id: str
    destination_depot_id: str
    distance: float
    average_time: float
    is_active: bool

    @field_validator("id", "source_depot_id", "destination_depot_id", mode="before")
    @classmethod
    def stringify_ids(cls, v) -> str:
        return str(v)
