"""
Simulate the exact same database operations that the API performs
to see where the data is going
"""

import sys
import os
sys.path.insert(0, r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend')

# Import the same modules that the API uses
from backend.src.core.database import get_session, engine
from backend.src.services.todo_service import TodoService
from backend.src.models.task import TaskCreate
from uuid import UUID

# Create a task using the same service that the API uses
service = TodoService()

# Create a test user ID that exists in the database
test_user_id = UUID("3b63e1f6-67d8-4750-9c0b-493791869778")  # testuser@example.com

# Create task data
task_data = TaskCreate(
    title="API Simulation Test",
    description="Testing where the API actually saves data",
    completed=False
)

print("Using engine URL:", engine.url)
print("Creating task using TodoService...")

try:
    # Get a session the same way the API does
    session_gen = get_session()
    session = next(session_gen)

    # Create the task using the same method as the API
    created_task = service.create_todo(session, task_data, test_user_id)

    print(f"Task created successfully!")
    print(f"Task ID: {created_task.id}")
    print(f"Task Title: {created_task.title}")
    print(f"Task User ID: {created_task.user_id}")

    # Close the session
    session.close()

except Exception as e:
    print(f"Error creating task: {e}")
    import traceback
    traceback.print_exc()