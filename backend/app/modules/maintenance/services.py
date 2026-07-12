from datetime import datetime
from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from beanie import PydanticObjectId

from app.modules.vehicles.models import Vehicle, VehicleStatus
from .models import Maintenance, MaintenanceStatus


class MaintenanceService:

    async def create_maintenance(self, data):
        try:
            v_id = PydanticObjectId(data.vehicle_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid vehicle ID format"
            )

        vehicle = await Vehicle.get(v_id)
        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found"
            )

        maintenance = Maintenance(
            vehicle_id=v_id,
            maintenance_type=data.maintenance_type,
            description=data.description,
            service_due_at=data.service_due_at
        )

        await maintenance.insert()

        vehicle.status = VehicleStatus.IN_MAINTENANCE
        await vehicle.save()

        return maintenance

    async def get_all_maintenance(self):
        return await Maintenance.find().to_list()

    async def get_maintenance(self, maintenance_id: str):
        try:
            m_id = PydanticObjectId(maintenance_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid maintenance ID format"
            )

        maintenance = await Maintenance.get(m_id)
        if maintenance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance not found"
            )
        return maintenance

    async def start_maintenance(self, maintenance_id: str):
        try:
            m_id = PydanticObjectId(maintenance_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid maintenance ID format"
            )

        maintenance = await Maintenance.get(m_id)
        if maintenance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance not found"
            )

        maintenance.status = MaintenanceStatus.IN_PROGRESS
        maintenance.started_at = datetime.utcnow()
        await maintenance.save()

        return maintenance

    async def complete_maintenance(self, maintenance_id: str, cost: float):
        try:
            m_id = PydanticObjectId(maintenance_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid maintenance ID format"
            )

        maintenance = await Maintenance.get(m_id)
        if maintenance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance not found"
            )

        vehicle = await Vehicle.get(maintenance.vehicle_id)

        maintenance.status = MaintenanceStatus.COMPLETED
        maintenance.completed_at = datetime.utcnow()
        maintenance.cost = cost
        await maintenance.save()

        if vehicle:
            vehicle.status = VehicleStatus.AVAILABLE
            await vehicle.save()

        return maintenance
