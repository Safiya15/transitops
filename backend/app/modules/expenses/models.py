from datetime import datetime
from enum import Enum
from typing import Optional

# pyrefly: ignore [missing-import]
from beanie import Document, PydanticObjectId
from pydantic import Field


class ExpenseCategory(str, Enum):
    TOLL = "Toll"
    PARKING = "Parking"
    REPAIR = "Repair"
    INSURANCE = "Insurance"
    OTHER = "Other"


class Expense(Document):

    vehicle_id: PydanticObjectId

    trip_id: Optional[PydanticObjectId] = None

    category: ExpenseCategory

    amount: float = Field(gt=0)

    description: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    class Settings:
        name = "expenses"
