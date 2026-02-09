from pydantic_settings import BaseSettings
from typing import List, Optional
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables from .env file before creating settings
load_dotenv()

# Check environment variables directly to ensure Neon is prioritized
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

# Determine the database URL to use - prioritize Neon
FINAL_DATABASE_URL = NEON_DATABASE_URL if NEON_DATABASE_URL else DATABASE_URL
if not FINAL_DATABASE_URL:
    # Only fallback to SQLite if neither environment variable is set
    FINAL_DATABASE_URL = "sqlite:///./todo_app.db"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Project information
    project_name: str = "Secure Todo API"
    version: str = "1.0.0"
    description: str = "Secure Multi-User Todo Web Application with JWT Authentication"

    # API settings
    api_v1_prefix: str = "/api/v1"

    # Database settings - use the final determined database URL
    database_url: str = FINAL_DATABASE_URL
    neon_database_url: Optional[str] = NEON_DATABASE_URL
    database_echo: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-jwt-signing-key-here-make-it-long-and-random")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # CORS settings
    backend_cors_origins: List[str] = [
        "http://localhost:3000",  # Frontend dev server
        "http://localhost:3001",  # Frontend dev server on port 3001
        "http://localhost:3002",  # Frontend dev server on port 3002
        "http://localhost:3003",  # Frontend dev server on port 3003
        "http://localhost:8000",  # Backend dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
        "http://127.0.0.1:8000",
        "https://localhost:3000",
        "https://localhost:3001",
        "https://localhost:3002",
        "https://localhost:3003",
        "https://localhost:8000",
    ]

    # Logging settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Better Auth settings
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "http://localhost:8000")

    model_config = {
        "env_file": ".env",  # This will still be used for other settings
        "case_sensitive": True,
        "extra": "ignore"
    }


# Create settings instance
settings = Settings()


# Error handling and exception handlers
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging


def setup_logging():
    """
    Configure application logging.
    """
    logging.basicConfig(
        level=settings.log_level.upper(),
        format=settings.log_format
    )


def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions and return JSON responses.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail if hasattr(exc, 'detail') else "An error occurred"
            }
        }
    )


def validation_exception_handler(request: Request, exc: Exception):
    """
    Handle validation exceptions and return JSON responses.
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation error occurred",
                "details": str(exc)
            }
        }
    )


def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions and return JSON responses.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred"
            }
        }
    )


# Initialize logging
setup_logging()