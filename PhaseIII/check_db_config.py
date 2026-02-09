import os
from backend.src.core.config import settings

print("Database Configuration Analysis:")
print(f"DATABASE_URL from env: {os.getenv('DATABASE_URL', 'Not set')}")
print(f"NEON_DATABASE_URL from env: {os.getenv('NEON_DATABASE_URL', 'Not set')}")
print(f"settings.database_url: {settings.database_url}")
print(f"settings.neon_database_url: {settings.neon_database_url}")

# Check which database is being used
if settings.neon_database_url:
    print("\nAccording to the code logic:")
    print("- neon_database_url is set, so DATABASE_URL should be set to neon_database_url")
    print("- This means the backend SHOULD use the Neon PostgreSQL database")
else:
    print("\nAccording to the code logic:")
    print("- neon_database_url is NOT set, so the backend will use the default SQLite database")

print(f"\nCurrent database being used: {settings.database_url}")
if "postgresql" in settings.database_url.lower():
    print("-> Using PostgreSQL (Neon)")
elif "sqlite" in settings.database_url.lower():
    print("-> Using SQLite")
else:
    print("-> Using unknown database type")