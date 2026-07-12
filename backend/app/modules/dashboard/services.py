from app.modules.vehicles.models import Vehicle, VehicleStatus
from app.modules.drivers.models import Driver, DriverStatus
from app.modules.trips.models import Trip, TripStatus
from app.modules.fuel.models import FuelLog
from app.modules.expenses.models import Expense
from app.modules.maintenance.models import Maintenance, MaintenanceStatus


class DashboardService:

    async def get_dashboard(self):
        total_vehicles = await Vehicle.count()

        available_vehicles = await Vehicle.find(
            Vehicle.status == VehicleStatus.AVAILABLE
        ).count()

        vehicles_on_trip = await Vehicle.find(
            Vehicle.status == VehicleStatus.ON_TRIP
        ).count()

        vehicles_in_maintenance = await Vehicle.find(
            Vehicle.status == VehicleStatus.IN_MAINTENANCE
        ).count()

        total_drivers = await Driver.count()

        available_drivers = await Driver.find(
            Driver.status == DriverStatus.AVAILABLE
        ).count()

        active_trips = await Trip.find(
            Trip.status == TripStatus.IN_PROGRESS
        ).count()

        completed_trips = await Trip.find(
            Trip.status == TripStatus.COMPLETED
        ).count()

        maintenance_due = await Maintenance.find(
            Maintenance.status == MaintenanceStatus.PENDING
        ).count()

        fuel_logs = await FuelLog.find().to_list()
        expenses = await Expense.find().to_list()

        total_fuel_cost = sum(fuel.cost for fuel in fuel_logs)
        total_expense = sum(expense.amount for expense in expenses)

        if fuel_logs:
            average_fuel_efficiency = (
                sum(fuel.fuel_efficiency for fuel in fuel_logs) / len(fuel_logs)
            )
        else:
            average_fuel_efficiency = 0

        return {
            "total_vehicles": total_vehicles,
            "available_vehicles": available_vehicles,
            "vehicles_on_trip": vehicles_on_trip,
            "vehicles_in_maintenance": vehicles_in_maintenance,
            "total_drivers": total_drivers,
            "available_drivers": available_drivers,
            "active_trips": active_trips,
            "completed_trips": completed_trips,
            "total_fuel_cost": total_fuel_cost,
            "total_expense": total_expense,
            "average_fuel_efficiency": round(average_fuel_efficiency, 2),
            "maintenance_due": maintenance_due
        }
