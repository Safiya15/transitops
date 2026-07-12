from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

from .models import UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def stringify_id(cls, v) -> str:
        return str(v)


class UpdateUserRoleRequest(BaseModel):
    role: UserRole


class UpdateUserStatusRequest(BaseModel):
    is_active: bool
