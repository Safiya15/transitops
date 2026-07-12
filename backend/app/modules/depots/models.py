from datetime import datetime

# pyrefly: ignore [missing-import]
from beanie import Document
from pymongo import IndexModel, ASCENDING
from pydantic import Field


class Depot(Document):

    name: str

    city: str

    state: str

    address: str

    latitude: float

    longitude: float

    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "depots"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]
