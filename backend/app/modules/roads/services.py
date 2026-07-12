from datetime import datetime
from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from beanie import PydanticObjectId

from app.modules.depots.models import Depot
from .models import Road
from .schemas import UpdateRoadRequest


class RoadService:

    async def create_road(self, data):
        try:
            source_id = PydanticObjectId(data.source_depot_id)
            dest_id = PydanticObjectId(data.destination_depot_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid depot ID format"
            )

        source = await Depot.get(source_id)
        destination = await Depot.get(dest_id)

        if not source or not destination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source or destination depot not found"
            )

        existing = await Road.find_one(
            Road.source_depot_id == source.id,
            Road.destination_depot_id == destination.id
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Road already exists"
            )

        road = Road(
            source_depot_id=source.id,
            destination_depot_id=destination.id,
            distance=data.distance,
            average_time=data.average_time
        )

        await road.insert()
        return road

    async def get_all_roads(self):
        return await Road.find().to_list()

    async def get_road(self, road_id: str):
        try:
            r_id = PydanticObjectId(road_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid road ID format"
            )

        road = await Road.get(r_id)
        if not road:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Road not found"
            )
        return road

    async def update_road(self, road_id: str, data: UpdateRoadRequest):
        try:
            r_id = PydanticObjectId(road_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid road ID format"
            )

        road = await Road.get(r_id)
        if not road:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Road not found"
            )

        road.distance = data.distance
        road.average_time = data.average_time
        road.updated_at = datetime.utcnow()

        await road.save()
        return road

    async def deactivate_road(self, road_id: str):
        try:
            r_id = PydanticObjectId(road_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid road ID format"
            )

        road = await Road.get(r_id)
        if not road:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Road not found"
            )

        road.is_active = False
        road.updated_at = datetime.utcnow()
        await road.save()
        return road
