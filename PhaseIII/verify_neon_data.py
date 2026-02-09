import sys
sys.path.insert(0, r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend')

from backend.src.core.database import Session, engine
from backend.src.models.task import Task
from sqlmodel import select

# Connect directly to the configured engine
with Session(engine) as session:
    # Query for all tasks
    statement = select(Task)
    result = session.exec(statement)
    tasks = result.all()

    print(f"Total tasks found in configured database: {len(tasks)}")

    # Show recent tasks
    for task in tasks[-5:]:  # Last 5 tasks
        print(f"  - ID: {task.id}, Title: {task.title}, User: {task.user_id}, Created: {task.created_at}")

    # Query for tasks with a specific title that should exist
    statement = select(Task).where(Task.title == "Fixed Backend - Neon Database")
    result = session.exec(statement)
    specific_tasks = result.all()

    print(f"\nTasks with title 'Fixed Backend - Neon Database': {len(specific_tasks)}")
    for task in specific_tasks:
        print(f"  - ID: {task.id}, Title: {task.title}, User: {task.user_id}, Created: {task.created_at}")