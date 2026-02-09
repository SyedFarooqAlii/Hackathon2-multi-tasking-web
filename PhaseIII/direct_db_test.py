import sys
import os
sys.path.insert(0, r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend')

# Import the database engine
from backend.src.core.database import engine, Session
from backend.src.models.task import Task
from uuid import uuid4
from datetime import datetime

# Create a test task directly using the engine
try:
    # Create a session directly with the engine
    with Session(engine) as session:
        print("Connected to database successfully!")

        # Create a test task
        test_task = Task(
            id=uuid4(),  # Generate a new UUID
            title="Direct Database Test",
            description="This task was inserted directly using the database engine",
            completed=False,
            user_id=uuid4(),  # Generate a test user ID
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(test_task)
        session.commit()
        session.refresh(test_task)

        print(f"Task created successfully! ID: {test_task.id}")
        print(f"Task title: {test_task.title}")
        print(f"Task user_id: {test_task.user_id}")

        # Now let's query to see if it's there
        from sqlmodel import select
        stmt = select(Task).where(Task.title == "Direct Database Test")
        result = session.exec(stmt)
        found_tasks = result.all()

        print(f"Found {len(found_tasks)} tasks with the test title")
        for task in found_tasks:
            print(f"  - Task ID: {task.id}, Title: {task.title}")

except Exception as e:
    print(f"Error connecting to database or creating task: {e}")
    import traceback
    traceback.print_exc()