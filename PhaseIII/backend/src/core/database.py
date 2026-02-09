import os
from dotenv import load_dotenv

# Load environment variables FIRST, before any other imports that might use settings
load_dotenv()

from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

def get_engine():
    """
    Create SQLAlchemy engine at runtime with current DATABASE_URL.
    This ensures the engine always uses the current database configuration.
    """
    # Get the database URL directly from environment to avoid any caching issues
    neon_database_url = os.getenv("NEON_DATABASE_URL")
    database_url = os.getenv("DATABASE_URL")

    print(f"DEBUG get_engine(): NEON_DATABASE_URL = {neon_database_url}")
    print(f"DEBUG get_engine(): DATABASE_URL = {database_url}")

    # Use Neon if available, otherwise fall back to main database URL
    final_database_url = neon_database_url if neon_database_url else database_url

    print(f"DEBUG get_engine(): Final database URL being used: {final_database_url}")  # Debug line to see what URL is being used

    # Ensure we're using PostgreSQL/Neon, not SQLite
    if not ("postgresql" in final_database_url.lower() or "postgres" in final_database_url.lower()):
        print(f"ERROR: Expected PostgreSQL URL, got: {final_database_url}")
        raise AssertionError(f"Expected PostgreSQL URL, got: {final_database_url}")

    # Get other settings from environment directly
    echo = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    pool_size = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    max_overflow = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))

    return create_engine(
        final_database_url,
        echo=echo,  # Set to True for SQL query logging
        pool_pre_ping=True,  # Verify connections before use
        pool_size=pool_size,
        max_overflow=max_overflow
    )


def create_db_and_tables():
    """
    Initialize database connection.
    Table creation should be handled separately to avoid metadata binding issues.
    """
    engine = get_engine()  # Create fresh engine
    # Note: Avoiding metadata.create_all() to prevent binding to specific engine
    print("Database connection initialized with engine:", engine.url)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection in FastAPI endpoints.
    Creates a fresh engine and session at runtime to ensure correct database connection.
    """
    import datetime
    # Write to a file to make sure this is being called
    with open('C:/Users/PMLS/Desktop/hackathon2_phase1/PhaseII/backend/debug_log.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()}: get_session() called - creating fresh engine\n")
    print("DEBUG: get_session() called - creating fresh engine")  # Debug line
    engine = get_engine()  # Create fresh engine at runtime
    # Write the URL to the file as well
    with open('C:/Users/PMLS/Desktop/hackathon2_phase1/PhaseII/backend/debug_log.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()}: Using engine with URL: {engine.url}\n")
    print(f"DEBUG: Using engine with URL: {engine.url}")  # Debug line
    with Session(engine) as session:
        print(f"DEBUG: Session created with dialect: {session.bind.dialect.name}")  # Debug dialect
        print(f"DEBUG: Session bound to URL: {str(session.bind.url)}")  # Debug URL
        yield session