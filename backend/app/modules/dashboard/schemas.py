from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_vehicles: int
    available_vehicles: int
    vehicles_on_trip: int
    vehicles_in_maintenance: int
    total_drivers: int
    available_drivers: int
    active_trips: int
    completed_trips: int
    total_fuel_cost: float
    total_expense: float
    average_fuel_efficiency: float
    maintenance_due: int
