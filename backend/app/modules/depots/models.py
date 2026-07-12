from typing import Optional
from beanie import Document


class Depot(Document):
    name: str
    location: str
    capacity: Optional[int] = None     # number of vehicles it can hold
    manager: Optional[str] = None
    is_active: bool = True

    class Settings:
        name = "depots"
