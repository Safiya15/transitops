from typing import Optional
from datetime import datetime
from beanie import Document, Link
from app.modules.vehicles.models import Vehicle


class Maintenance(Document):
    vehicle: Optional[Link[Vehicle]] = None
    description: str
    cost: Optional[float] = None
    date: Optional[datetime] = None
    status: str = "pending"            # pending | in_progress | completed
    notes: Optional[str] = None

    class Settings:
        name = "maintenance"
