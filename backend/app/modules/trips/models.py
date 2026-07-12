from typing import Optional
from datetime import datetime
from beanie import Document, Link
from app.modules.vehicles.models import Vehicle
from app.modules.drivers.models import Driver
from app.modules.roads.models import Road


class Trip(Document):
    vehicle: Optional[Link[Vehicle]] = None
    driver: Optional[Link[Driver]] = None
    road: Optional[Link[Road]] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str = "scheduled"          # scheduled | in_progress | completed | cancelled
    notes: Optional[str] = None

    class Settings:
        name = "trips"
