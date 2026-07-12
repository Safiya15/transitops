from datetime import datetime

from fastapi import HTTPException, status

from .models import Vehicle
from .schemas import UpdateVehicleRequest


class VehicleService:

    async def create_vehicle(self, data):
        existing = await Vehicle.find_one(
            Vehicle.registration_number == data.registration_number
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vehicle already exists",
            )

        vehicle = Vehicle(
            registration_number=data.registration_number,
            manufacturer=data.manufacturer,
            model=data.model,
            vehicle_type=data.vehicle_type,
            capacity=data.capacity,
            purchase_cost=data.purchase_cost,
        )

        await vehicle.insert()
        return vehicle

    async def get_all_vehicles(self):
        return await Vehicle.find().to_list()

    async def get_vehicle(self, vehicle_id: str):
        vehicle = await Vehicle.get(vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found",
            )
        return vehicle

    async def update_vehicle(self, vehicle_id: str, data: UpdateVehicleRequest):
        vehicle = await Vehicle.get(vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found",
            )

        vehicle.manufacturer = data.manufacturer
        vehicle.model = data.model
        vehicle.vehicle_type = data.vehicle_type
        vehicle.capacity = data.capacity
        vehicle.purchase_cost = data.purchase_cost
        vehicle.updated_at = datetime.utcnow()

        await vehicle.save()
        return vehicle

    async def delete_vehicle(self, vehicle_id: str):
        vehicle = await Vehicle.get(vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found",
            )
        await vehicle.delete()
