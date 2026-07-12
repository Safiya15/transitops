from typing import Optional
from datetime import datetime
from beanie import Document, Link
from app.modules.vehicles.models import Vehicle


class FuelLog(Document):
    vehicle: Optional[Link[Vehicle]] = None
    liters: float
    cost_per_liter: float
    total_cost: float
    odometer_reading: Optional[float] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

    class Settings:
        name = "fuel_logs"
