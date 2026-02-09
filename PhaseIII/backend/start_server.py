import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Change to the backend directory
os.chdir(r"C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend")

# Start the uvicorn server
try:
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "src.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"  # This enables auto-reload for development
    ])
except KeyboardInterrupt:
    print("Server stopped.")