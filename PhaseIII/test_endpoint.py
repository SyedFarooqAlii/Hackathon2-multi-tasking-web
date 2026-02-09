# Add a temporary test endpoint to the API to check database configuration
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from backend.src.core.config import settings
from backend.src.core.database import engine

print("=== Database Configuration Check ===")
print(f"DATABASE_URL environment variable: {os.getenv('DATABASE_URL', 'Not set')}")
print(f"NEON_DATABASE_URL environment variable: {os.getenv('NEON_DATABASE_URL', 'Not set')}")
print(f"Settings database_url: {settings.database_url}")
print(f"Settings neon_database_url: {settings.neon_database_url}")
print(f"Actual engine URL: {engine.url}")
print("===================================")

if "postgresql" in str(engine.url).lower():
    print("✓ Database engine is configured for PostgreSQL (Neon)")
elif "sqlite" in str(engine.url).lower():
    print("✗ Database engine is configured for SQLite")
else:
    print("? Unknown database engine")