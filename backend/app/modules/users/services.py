from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.modules.auth.schemas import CreateUserRequest

from .models import User, UserRole


class UserService:

    async def get_all_users(self):
        return await User.find().to_list()

    async def get_user(self, user_id: str):
        user = await User.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def create_user(self, data: CreateUserRequest):
        existing = await User.find_one(User.email == data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password),
            role=UserRole.DISPATCHER,
        )
        await user.insert()
        return {"message": "User created successfully"}

    async def update_role(self, user_id: str, role: UserRole):
        user = await User.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        user.role = role
        await user.save()
        return user

    async def update_status(self, user_id: str, is_active: bool):
        user = await User.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        user.is_active = is_active
        await user.save()
        return user

    async def delete_user(self, user_id: str):
        user = await User.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        await user.delete()
