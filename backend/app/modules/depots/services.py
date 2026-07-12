from datetime import datetime
from fastapi import HTTPException, status
from .models import Depot
from .schemas import UpdateDepotRequest


class DepotService:

    async def create_depot(self, data):
        existing = await Depot.find_one(Depot.name == data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Depot already exists"
            )

        depot = Depot(**data.model_dump())
        await depot.insert()
        return depot

    async def get_all_depots(self):
        return await Depot.find().to_list()

    async def get_depot(self, depot_id: str):
        depot = await Depot.get(depot_id)
        if not depot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Depot not found"
            )
        return depot

    async def update_depot(self, depot_id: str, data: UpdateDepotRequest):
        depot = await Depot.get(depot_id)
        if not depot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Depot not found"
            )

        depot.name = data.name
        depot.city = data.city
        depot.state = data.state
        depot.address = data.address
        depot.latitude = data.latitude
        depot.longitude = data.longitude
        depot.is_active = data.is_active
        depot.updated_at = datetime.utcnow()

        await depot.save()
        return depot

    async def deactivate_depot(self, depot_id: str):
        depot = await Depot.get(depot_id)
        if depot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Depot not found"
            )

        depot.is_active = False
        depot.updated_at = datetime.utcnow()
        await depot.save()
        return depot
