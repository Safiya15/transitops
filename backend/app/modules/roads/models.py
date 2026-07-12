from datetime import datetime

# pyrefly: ignore [missing-import]
from beanie import Document, PydanticObjectId
from pymongo import IndexModel, ASCENDING
from pydantic import Field


class Road(Document):

    source_depot_id: PydanticObjectId

    destination_depot_id: PydanticObjectId

    distance: float = Field(gt=0)

    average_time: float = Field(gt=0)

    is_active: bool = True

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        name = "roads"
        indexes = [
            IndexModel(
                [
                    ("source_depot_id", ASCENDING),
                    ("destination_depot_id", ASCENDING)
                ],
                unique=True
            )
        ]