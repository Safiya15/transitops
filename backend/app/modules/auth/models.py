from datetime import datetime
from typing import List

# pyrefly: ignore [missing-import]
from beanie import Document
from pymongo import IndexModel, ASCENDING
from pydantic import Field


class Role(Document):

    name: str = Field(
        ...,
        min_length=3,
        max_length=30
    )

    description: str

    permissions: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "roles"
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]
