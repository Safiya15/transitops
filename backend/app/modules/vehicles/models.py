from typing import Optional
from beanie import Document


class Vehicle(Document):
    registration_number: str
    make: str
    model: str
    year: int
    capacity: int                      # passenger or cargo capacity
    fuel_type: str = "diesel"
    is_active: bool = True

    class Settings:
        name = "vehicles"
