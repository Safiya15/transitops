from datetime import datetime
from enum import Enum

# pyrefly: ignore [missing-import]
from beanie import Document
from pymongo import IndexModel, ASCENDING
from pydantic import Field


class DriverStatus(str, Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    SUSPENDED = "Suspended"
    INACTIVE = "Inactive"


class LicenseCategory(str, Enum):
    LMV = "LMV"
    HMV = "HMV"
    MCWG = "MCWG"


class Driver(Document):

    name: str

    phone_number: str

    email: str

    license_number: str

    license_category: LicenseCategory

    license_expiry: datetime

    safety_score: float = 100

    status: DriverStatus = DriverStatus.AVAILABLE

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "drivers"
        indexes = [
            IndexModel([("phone_number", ASCENDING)], unique=True),
            IndexModel([("email", ASCENDING)], unique=True),
            IndexModel([("license_number", ASCENDING)], unique=True),
        ]
