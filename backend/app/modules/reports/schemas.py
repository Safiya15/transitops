from pydantic import BaseModel


class FleetSummaryResponse(BaseModel):
    total_vehicles: int
    active_trips: int
    total_drivers: int
    total_distance: float
    total_fuel_cost: float
    total_expenses: float


class VehicleReportResponse(BaseModel):
    total_trips: int
    total_distance: float
    fuel_cost: float
    expense_cost: float
    maintenance_count: int


class FuelReportResponse(BaseModel):
    total_logs: int
    total_cost: float
    average_efficiency: float


class ExpenseReportResponse(BaseModel):
    total_expenses: int
    total_cost: float


class MaintenanceReportResponse(BaseModel):
    total_records: int
    completed: int
    pending: int
