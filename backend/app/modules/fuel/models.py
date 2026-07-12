from datetime import datetime

# pyrefly: ignore [missing-import]
from beanie import Document, PydanticObjectId
from pymongo import IndexModel, ASCENDING
from pydantic import Field


class FuelLog(Document):

    vehicle_id: PydanticObjectId

    trip_id: PydanticObjectId

    litres: float = Field(gt=0)

    cost: float = Field(gt=0)

    price_per_litre: float

    fuel_efficiency: float

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        name = "fuel_logs"
        indexes = [
            IndexModel([("trip_id", ASCENDING)], unique=True)
        ]
