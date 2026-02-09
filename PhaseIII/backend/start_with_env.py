import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

print(f"DATABASE_URL from environment: {os.getenv('DATABASE_URL', 'Not set')}")
print(f"NEON_DATABASE_URL from environment: {os.getenv('NEON_DATABASE_URL', 'Not set')}")

# Now import and start the application
from uvicorn import Config, Server
from backend.src.main import app

if __name__ == "__main__":
    config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config=config)
    server.run()