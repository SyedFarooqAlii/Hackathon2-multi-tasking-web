from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.api import router as api_v1_router
from .core.database import create_db_and_tables
from contextlib import asynccontextmanager
from typing import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler to run startup and shutdown events.
    """
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: Cleanup operations can be added here if needed


# Create the FastAPI application
app = FastAPI(
    title=settings.project_name,
    description="Secure Multi-User Todo Web Application with JWT Authentication",
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],  # This allows all headers including Authorization
    )

# Include API routers
app.include_router(api_v1_router, prefix=settings.api_v1_prefix, tags=["v1"])

@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Secure Todo API is running!"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is operational.
    """
    return {"status": "healthy", "version": settings.version}