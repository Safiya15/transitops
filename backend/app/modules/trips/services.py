from datetime import datetime, timezone
from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from beanie import PydanticObjectId

from app.modules.drivers.models import Driver, DriverStatus
from app.modules.vehicles.models import Vehicle, VehicleStatus
from app.modules.trips.models import Trip, TripStatus
from app.modules.routing.route_service import RouteService


class TripService:

    def __init__(self):
        self.route_service = RouteService()

    async def validate_vehicle(self, vehicle_id: PydanticObjectId, cargo_weight: float) -> Vehicle:
        vehicle = await Vehicle.get(vehicle_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found"
            )

        if vehicle.status != VehicleStatus.AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle is unavailable"
            )

        if cargo_weight > vehicle.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cargo exceeds vehicle capacity"
            )

        return vehicle

    async def validate_driver(self, driver_id: PydanticObjectId) -> Driver:
        driver = await Driver.get(driver_id)
        if driver is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )

        if driver.status != DriverStatus.AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver unavailable"
            )

        # Naive datetime comparison to prevent TypeError
        expiry = driver.license_expiry.replace(tzinfo=None) if driver.license_expiry.tzinfo else driver.license_expiry
        if expiry < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver license expired"
            )

        return driver

    async def create_trip(self, data):
        try:
            v_id = PydanticObjectId(data.vehicle_id)
            d_id = PydanticObjectId(data.driver_id)
            s_depot_id = PydanticObjectId(data.source_depot_id)
            d_depot_id = PydanticObjectId(data.destination_depot_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid ID format"
            )

        vehicle = await self.validate_vehicle(v_id, data.cargo_weight)
        driver = await self.validate_driver(d_id)

        route = await self.route_service.calculate_route(
            data.source_depot_id,
            data.destination_depot_id
        )

        trip = Trip(
            vehicle_id=v_id,
            driver_id=d_id,
            source_depot_id=s_depot_id,
            destination_depot_id=d_depot_id,
            route=[PydanticObjectId(node) for node in route["path"]],
            total_distance=route["distance"],
            estimated_time=route["estimated_time"],
            cargo_weight=data.cargo_weight
        )

        await trip.insert()

        vehicle.status = VehicleStatus.ON_TRIP
        await vehicle.save()

        driver.status = DriverStatus.ON_TRIP
        await driver.save()

        return trip

    async def complete_trip(self, trip_id: str):
        try:
            t_id = PydanticObjectId(trip_id)
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

        if trip.status == TripStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Trip is already completed"
            )

        vehicle = await Vehicle.get(trip.vehicle_id)
        driver = await Driver.get(trip.driver_id)

        trip.status = TripStatus.COMPLETED
        trip.completed_at = datetime.utcnow()
        await trip.save()

        if vehicle:
            vehicle.status = VehicleStatus.AVAILABLE
            vehicle.odometer += trip.total_distance
            await vehicle.save()

        if driver:
            driver.status = DriverStatus.AVAILABLE
            await driver.save()

        return trip

    async def cancel_trip(self, trip_id: str):
        try:
            t_id = PydanticObjectId(trip_id)
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

        if trip.status in [TripStatus.COMPLETED, TripStatus.CANCELLED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel completed or already cancelled trip"
            )

        trip.status = TripStatus.CANCELLED
        await trip.save()

        # Free vehicle and driver
        vehicle = await Vehicle.get(trip.vehicle_id)
        if vehicle:
            vehicle.status = VehicleStatus.AVAILABLE
            await vehicle.save()

        driver = await Driver.get(trip.driver_id)
        if driver:
            driver.status = DriverStatus.AVAILABLE
            await driver.save()

        return trip

    async def get_trip(self, trip_id: str):
        try:
            t_id = PydanticObjectId(trip_id)
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

        return trip

    async def get_all_trips(self):
        return await Trip.find().to_list()
