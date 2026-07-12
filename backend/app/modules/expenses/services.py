from fastapi import HTTPException, status
# pyrefly: ignore [missing-import]
from beanie import PydanticObjectId

from app.modules.vehicles.models import Vehicle
from app.modules.trips.models import Trip
from .models import Expense


class ExpenseService:

    async def create_expense(self, data):
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

        t_id = None
        if data.trip_id:
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

        expense = Expense(
            vehicle_id=vehicle.id,
            trip_id=t_id,
            category=data.category,
            amount=data.amount,
            description=data.description
        )

        await expense.insert()
        return expense

    async def get_all_expenses(self):
        return await Expense.find().to_list()

    async def vehicle_expenses(self, vehicle_id: str):
        try:
            v_id = PydanticObjectId(vehicle_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid vehicle ID format"
            )
        return await Expense.find(Expense.vehicle_id == v_id).to_list()

    async def trip_expenses(self, trip_id: str):
        try:
            t_id = PydanticObjectId(trip_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid trip ID format"
            )
        return await Expense.find(Expense.trip_id == t_id).to_list()
