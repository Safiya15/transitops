from datetime import datetime

from fastapi import HTTPException, status

from .models import Driver
from .schemas import UpdateDriverRequest


class DriverService:

    async def create_driver(self, data):
        existing = await Driver.find_one(
            Driver.license_number == data.license_number
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Driver already exists",
            )

        new_driver = Driver(**data.model_dump())
        await new_driver.insert()
        return new_driver

    async def get_all_drivers(self):
        return await Driver.find().to_list()

    async def get_driver(self, driver_id: str):
        driver = await Driver.get(driver_id)
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found",
            )
        return driver

    async def update_driver(self, driver_id: str, data: UpdateDriverRequest):
        driver = await Driver.get(driver_id)
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found",
            )

        driver.name = data.name
        driver.phone_number = data.phone_number
        driver.email = data.email
        driver.license_category = data.license_category
        driver.license_expiry = data.license_expiry
        driver.safety_score = data.safety_score
        driver.updated_at = datetime.utcnow()

        await driver.save()
        return driver

    async def delete_driver(self, driver_id: str):
        driver = await Driver.get(driver_id)
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found",
            )
        await driver.delete()
