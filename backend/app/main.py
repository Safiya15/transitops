from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import connect_db, close_db

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
# from app.modules.vehicles.router    import router as vehicles_router
# from app.modules.drivers.router     import router as drivers_router
# from app.modules.depots.router      import router as depots_router
# from app.modules.roads.router       import router as roads_router
# from app.modules.trips.router       import router as trips_router
# from app.modules.maintenance.router import router as maintenance_router
# from app.modules.fuel.router        import router as fuel_router
# from app.modules.expenses.router    import router as expenses_router


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
# Include routers
# ---------------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(users_router)
# app.include_router(vehicles_router)
# app.include_router(drivers_router)
# app.include_router(depots_router)
# app.include_router(roads_router)
# app.include_router(trips_router)
# app.include_router(maintenance_router)
# app.include_router(fuel_router)
# app.include_router(expenses_router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
async def root():
    return {"message": "TransitOps API Running"}
