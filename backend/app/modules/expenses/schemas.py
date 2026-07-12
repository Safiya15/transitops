from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .models import ExpenseCategory


class CreateExpenseRequest(BaseModel):
    vehicle_id: str
    trip_id: Optional[str] = None
    category: ExpenseCategory
    amount: float = Field(gt=0)
    description: str


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vehicle_id: str
    trip_id: Optional[str] = None
    category: ExpenseCategory
    amount: float
    description: str
    created_at: datetime

    @field_validator("id", "vehicle_id", "trip_id", mode="before")
    @classmethod
    def stringify_ids(cls, v) -> Optional[str]:
        if v is None:
            return None
        return str(v)
