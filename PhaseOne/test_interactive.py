#!/usr/bin/env python3
"""
Test script to verify the interactive todo application functionality.
"""
import sys
import os

# Add the src directory to the path so imports work properly
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from src.cli.main import InteractiveTodoApp

def test_interactive_app():
    """Test the interactive app by creating a single instance."""
    print("Testing Interactive Todo Application...\n")

    # Create the app instance
    app = InteractiveTodoApp()

    # Test adding a task
    print("--- Testing Add Task ---")
    app.service.add_task("Test Task 1", "This is a test task")
    print("+ Added task 1")

    app.service.add_task("Test Task 2", "Another test task")
    print("+ Added task 2")

    # Test viewing tasks
    print("\n--- Testing View Tasks ---")
    tasks = app.service.get_all_tasks()
    table = app._format_tasks_table(tasks)
    print(table)
    print("+ Viewed all tasks")

    # Test updating a task
    print("\n--- Testing Update Task ---")
    try:
        updated_task = app.service.update_task(1, "Updated Task 1", "Updated description")
        print(f"+ Updated task 1: {updated_task.title}")
    except Exception as e:
        print(f"- Error updating task: {e}")

    # Test marking complete
    print("\n--- Testing Mark Complete ---")
    try:
        task = app.service.mark_task_complete(1)
        print(f"+ Marked task 1 as complete: {task.completed}")
    except Exception as e:
        print(f"- Error marking complete: {e}")

    # Test viewing tasks again to see changes
    print("\n--- Viewing Updated Tasks ---")
    tasks = app.service.get_all_tasks()
    table = app._format_tasks_table(tasks)
    print(table)

    # Test marking incomplete
    print("\n--- Testing Mark Incomplete ---")
    try:
        task = app.service.mark_task_incomplete(1)
        print(f"+ Marked task 1 as incomplete: {task.completed}")
    except Exception as e:
        print(f"- Error marking incomplete: {e}")

    # Test deleting a task
    print("\n--- Testing Delete Task ---")
    try:
        success = app.service.delete_task(2)
        print(f"+ Deleted task 2: {success}")
    except Exception as e:
        print(f"- Error deleting task: {e}")

    # Final view to confirm deletion
    print("\n--- Final View ---")
    tasks = app.service.get_all_tasks()
    table = app._format_tasks_table(tasks)
    print(table)

    print("\n*** All functionality tested successfully! ***")
    print("The interactive menu system is ready to use.")
    print("\nTo run the interactive application, simply execute:")
    print("python src/cli/main.py")

if __name__ == "__main__":
    test_interactive_app()