from datetime import datetime
from enum import Enum

# pyrefly: ignore [missing-import]
from beanie import Document
from pymongo import IndexModel, ASCENDING
from pydantic import Field


class VehicleStatus(str, Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    IN_MAINTENANCE = "In Maintenance"
    RETIRED = "Retired"


class VehicleType(str, Enum):
    TRUCK = "Truck"
    VAN = "Van"
    MINI_TRUCK = "Mini Truck"
    PICKUP = "Pickup"


class Vehicle(Document):

    registration_number: str

    model: str

    manufacturer: str

    vehicle_type: VehicleType

    capacity: float

    odometer: float = 0

    purchase_cost: float

    status: VehicleStatus = VehicleStatus.AVAILABLE

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "vehicles"
        indexes = [
            IndexModel([("registration_number", ASCENDING)], unique=True)
        ]
