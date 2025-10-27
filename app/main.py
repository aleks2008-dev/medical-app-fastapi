from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.infrastructure.database.postgres import engine
from app.infrastructure.database.models import Base
from app.infrastructure.redis import close_redis
from app.api.routers.doctors import router as doctors_router
from app.api.routers.users import router as users_router
from app.api.routers.appoointments import router as appointments_router
from app.api.routers.auth import router as auth_router
from app.api.routers.rooms import router as rooms_router

from app.use_cases.exceptions import DomainException
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Medical App")
    
    # Create database tables
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
    
    yield  # Здесь приложение работает
    
    # Shutdown
    logger.info("Shutting down Medical App")
    await engine.dispose()
    await close_redis()

app = FastAPI(title="Medical App", version="1.0.0", lifespan=lifespan)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(doctors_router, prefix="/api/v1", tags=["doctors"])
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(appointments_router, prefix="/api/v1", tags=["appointments"])
app.include_router(rooms_router, prefix="/api/v1", tags=["rooms"])


@app.get("/")
async def root():
    return {"message": "Medical App with PostgreSQL"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "postgresql"}

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)},
    )