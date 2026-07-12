from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from beanie import PydanticObjectId

from app.modules.vehicles.models import Vehicle
from app.modules.drivers.models import Driver
from app.modules.trips.models import Trip, TripStatus
from app.modules.fuel.models import FuelLog
from app.modules.expenses.models import Expense
from app.modules.maintenance.models import Maintenance, MaintenanceStatus


class ReportService:

    async def fleet_summary(self):
        vehicles = await Vehicle.count()
        drivers = await Driver.count()
        trips = await Trip.find().to_list()
        fuel_logs = await FuelLog.find().to_list()
        expenses = await Expense.find().to_list()

        total_distance = sum(trip.total_distance for trip in trips)
        total_fuel_cost = sum(fuel.cost for fuel in fuel_logs)
        total_expense = sum(expense.amount for expense in expenses)

        active_trips = len([
            trip for trip in trips
            if trip.status == TripStatus.IN_PROGRESS
        ])

        return {
            "total_vehicles": vehicles,
            "active_trips": active_trips,
            "total_drivers": drivers,
            "total_distance": total_distance,
            "total_fuel_cost": total_fuel_cost,
            "total_expenses": total_expense
        }

    async def vehicle_report(self, vehicle_id: str):
        try:
            v_id = PydanticObjectId(vehicle_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid vehicle ID format"
            )

        trips = await Trip.find(Trip.vehicle_id == v_id).to_list()
        fuel = await FuelLog.find(FuelLog.vehicle_id == v_id).to_list()
        expenses = await Expense.find(Expense.vehicle_id == v_id).to_list()
        maintenance = await Maintenance.find(Maintenance.vehicle_id == v_id).to_list()

        return {
            "total_trips": len(trips),
            "total_distance": sum(t.total_distance for t in trips),
            "fuel_cost": sum(f.cost for f in fuel),
            "expense_cost": sum(e.amount for e in expenses),
            "maintenance_count": len(maintenance)
        }

    async def fuel_report(self):
        logs = await FuelLog.find().to_list()
        total_cost = sum(log.cost for log in logs)

        if logs:
            average_efficiency = (
                sum(log.fuel_efficiency for log in logs) / len(logs)
            )
        else:
            average_efficiency = 0

        return {
            "total_logs": len(logs),
            "total_cost": total_cost,
            "average_efficiency": round(average_efficiency, 2)
        }

    async def expense_report(self):
        expenses = await Expense.find().to_list()
        return {
            "total_expenses": len(expenses),
            "total_cost": sum(expense.amount for expense in expenses)
        }

    async def maintenance_report(self):
        maintenance = await Maintenance.find().to_list()

        completed = len([
            m for m in maintenance
            if m.status == MaintenanceStatus.COMPLETED
        ])

        pending = len([
            m for m in maintenance
            if m.status == MaintenanceStatus.PENDING
        ])

        return {
            "total_records": len(maintenance),
            "completed": completed,
            "pending": pending
        }
