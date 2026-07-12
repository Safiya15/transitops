from typing import Optional
from beanie import Document


class Road(Document):
    name: str
    origin: str
    destination: str
    distance_km: Optional[float] = None
    is_active: bool = True

    class Settings:
        name = "roads"
