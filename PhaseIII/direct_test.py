import sys
import os
sys.path.insert(0, r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend')

# Test the get_engine function directly
from backend.src.core.database import get_engine, get_session

print("Testing get_engine function...")
engine = get_engine()
print(f"Engine URL: {engine.url}")

print("\nTesting get_session function...")
session_gen = get_session()
session = next(session_gen)
print(f"Session bound to engine URL: {session.bind.url}")
session.close()