import sys
import os

# Add the backend src directory to the path
sys.path.insert(0, r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend')

# Change to the backend directory to ensure .env is loaded
os.chdir(r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend')

# Import the database engine and settings
from backend.src.core.database import engine, database_url
from backend.src.core.config import settings

print("Database Engine Configuration:")
print(f"Settings database_url: {settings.database_url}")
print(f"Settings neon_database_url: {settings.neon_database_url}")
print(f"database_url variable: {database_url}")
print(f"Engine URL: {engine.url}")

if "postgresql" in str(engine.url):
    print("-> Engine is configured to use PostgreSQL (Neon)")
elif "sqlite" in str(engine.url):
    print("-> Engine is configured to use SQLite")
else:
    print("-> Engine is configured to use unknown database type")