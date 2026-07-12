from typing import Optional
from beanie import Document


class Driver(Document):
    name: str
    license_number: str
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True

    class Settings:
        name = "drivers"
