from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from beanie import PydanticObjectId

from app.modules.trips.models import Trip
from app.modules.vehicles.models import Vehicle
from .models import FuelLog


class FuelService:

    async def create_fuel_log(self, data):
        try:
            t_id = PydanticObjectId(data.trip_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid trip ID format"
            )

        trip = await Trip.get(t_id)
        if trip is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )

        existing = await FuelLog.find_one(FuelLog.trip_id == trip.id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Fuel log already exists for this trip"
            )

        price = data.cost / data.litres
        # Avoid division by zero if total_distance is 0
        efficiency = (trip.total_distance / data.litres) if data.litres > 0 else 0

        fuel = FuelLog(
            vehicle_id=trip.vehicle_id,
            trip_id=trip.id,
            litres=data.litres,
            cost=data.cost,
            price_per_litre=price,
            fuel_efficiency=efficiency
        )

        await fuel.insert()
        return fuel

    async def get_all_logs(self):
        return await FuelLog.find().to_list()

    async def vehicle_history(self, vehicle_id: str):
        try:
            v_id = PydanticObjectId(vehicle_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid vehicle ID format"
            )

        return await FuelLog.find(FuelLog.vehicle_id == v_id).to_list()

    async def get_trip_log(self, trip_id: str):
        try:
            t_id = PydanticObjectId(trip_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid trip ID format"
            )

        log = await FuelLog.find_one(FuelLog.trip_id == t_id)
        if log is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fuel log not found"
            )
        return log
