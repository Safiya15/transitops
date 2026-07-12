from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from .models import DriverStatus, LicenseCategory


class CreateDriverRequest(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    license_number: str
    license_category: LicenseCategory
    license_expiry: datetime


class UpdateDriverRequest(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    license_category: LicenseCategory
    license_expiry: datetime
    safety_score: float


class DriverResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    phone_number: str
    email: EmailStr
    license_number: str
    license_category: LicenseCategory
    license_expiry: datetime
    safety_score: float
    status: DriverStatus
    created_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def stringify_id(cls, v) -> str:
        return str(v)
