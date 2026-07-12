from datetime import datetime
from enum import Enum

# pyrefly: ignore [missing-import]
from beanie import Document
from pymongo import IndexModel, ASCENDING
from pydantic import EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "Admin"
    FLEET_MANAGER = "Fleet Manager"
    DISPATCHER = "Dispatcher"
    SAFETY_OFFICER = "Safety Officer"
    FINANCIAL_ANALYST = "Financial Analyst"


class User(Document):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    email: EmailStr

    hashed_password: str

    role: UserRole

    is_active: bool = True

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True)
        ]
