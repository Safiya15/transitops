from typing import Optional
from datetime import datetime
from beanie import Document, Link
from app.modules.trips.models import Trip


class Expense(Document):
    trip: Optional[Link[Trip]] = None
    category: str                      # e.g. "fuel", "toll", "repair", "misc"
    amount: float
    description: Optional[str] = None
    date: Optional[datetime] = None
    approved: bool = False

    class Settings:
        name = "expenses"
