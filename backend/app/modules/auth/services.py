from fastapi import HTTPException, status

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.modules.users.models import User, UserRole

from .schemas import LoginRequest, CreateUserRequest


class AuthService:

    async def create_user(self, data: CreateUserRequest):

        existing_user = await User.find_one(User.email == data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        new_user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password),  # ✅ correct field name
            role=UserRole.DISPATCHER,
        )

        await new_user.insert()

        return {"message": "User created successfully"}

    async def login(self, data: LoginRequest):

        user = await User.find_one(User.email == data.email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(data.password, user.hashed_password):  # ✅ correct field name
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.value,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }
