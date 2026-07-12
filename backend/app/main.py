from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import connect_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="TransitOps",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routers  (uncomment as each module is ready)
# ---------------------------------------------------------------------------
# from app.modules.auth.routes      import router as auth_router
# from app.modules.users.routes     import router as users_router
# from app.modules.vehicles.routes  import router as vehicles_router
# from app.modules.drivers.routes   import router as drivers_router
# from app.modules.depots.routes    import router as depots_router
# from app.modules.roads.routes     import router as roads_router
# from app.modules.trips.routes     import router as trips_router
# from app.modules.maintenance.routes import router as maintenance_router
# from app.modules.fuel.routes      import router as fuel_router
# from app.modules.expenses.routes  import router as expenses_router

# app.include_router(auth_router,        prefix="/api/auth",        tags=["Auth"])
# app.include_router(users_router,       prefix="/api/users",       tags=["Users"])
# app.include_router(vehicles_router,    prefix="/api/vehicles",    tags=["Vehicles"])
# app.include_router(drivers_router,     prefix="/api/drivers",     tags=["Drivers"])
# app.include_router(depots_router,      prefix="/api/depots",      tags=["Depots"])
# app.include_router(roads_router,       prefix="/api/roads",       tags=["Roads"])
# app.include_router(trips_router,       prefix="/api/trips",       tags=["Trips"])
# app.include_router(maintenance_router, prefix="/api/maintenance",  tags=["Maintenance"])
# app.include_router(fuel_router,        prefix="/api/fuel",        tags=["Fuel"])
# app.include_router(expenses_router,    prefix="/api/expenses",    tags=["Expenses"])


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
async def root():
    return {"message": "TransitOps API Running"}
