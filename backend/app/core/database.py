from typing import Optional

# pyrefly: ignore [missing-import]
from motor.motor_asyncio import AsyncIOMotorClient
# pyrefly: ignore [missing-import]
from beanie import init_beanie

from app.core.config import settings

# Import all Beanie documents
from app.modules.auth.models import Role
from app.modules.users.models import User
from app.modules.vehicles.models import Vehicle
from app.modules.drivers.models import Driver
from app.modules.depots.models import Depot
from app.modules.roads.models import Road
from app.modules.trips.models import Trip
from app.modules.maintenance.models import Maintenance
from app.modules.fuel.models import FuelLog
from app.modules.expenses.models import Expense


client: Optional[AsyncIOMotorClient] = None


async def connect_db():
    """
    Connect to MongoDB and initialize Beanie.
    """

    global client

    client = AsyncIOMotorClient(settings.mongodb_url)

    database = client[settings.database_name]

    await init_beanie(
        database=database,
        document_models=[
            Role,
            User,
            Vehicle,
            Driver,
            Depot,
            Road,
            Trip,
            Maintenance,
            FuelLog,
            Expense,
        ],
    )

    print("✅ MongoDB Connected")


async def close_db():
    """
    Close MongoDB connection.
    """

    global client

    if client:
        client.close()
        print("❌ MongoDB Disconnected")