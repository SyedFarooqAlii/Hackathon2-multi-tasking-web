import os
import sys

# Add the backend src directory to the path so we can import the modules
sys.path.insert(0, r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend')

# Set the working directory to the backend to ensure .env is loaded
os.chdir(r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend')

# Import the settings after changing directory
from backend.src.core.config import settings

print("Database Configuration when server started:")
print(f"DATABASE_URL from env: {os.getenv('DATABASE_URL', 'Not set')}")
print(f"NEON_DATABASE_URL from env: {os.getenv('NEON_DATABASE_URL', 'Not set')}")
print(f"settings.database_url: {settings.database_url}")
print(f"settings.neon_database_url: {settings.neon_database_url}")

print(f"\nCurrent database being used: {settings.database_url}")
if "postgresql" in settings.database_url.lower():
    print("-> Using PostgreSQL (Neon)")
elif "sqlite" in settings.database_url.lower():
    print("-> Using SQLite")
else:
    print("-> Using unknown database type")