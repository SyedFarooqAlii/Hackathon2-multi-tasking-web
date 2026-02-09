#!/usr/bin/env python3
"""
Simple demonstration of the interactive todo application.
"""
import sys
import os

# Add the src directory to the path so imports work properly
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from src.cli.main import InteractiveTodoApp

def demo():
    """Demonstrate the interactive app functionality."""
    print("=== INTERACTIVE TODO APP DEMONSTRATION ===\n")

    # Create an app instance
    app = InteractiveTodoApp()

    print("1. Adding tasks...")
    task1 = app.service.add_task("Buy groceries", "Milk, bread, eggs, fruits")
    print(f"   Added task: ID {task1.id} - {task1.title}")

    task2 = app.service.add_task("Complete project", "Finish the todo app project")
    print(f"   Added task: ID {task2.id} - {task2.title}")

    task3 = app.service.add_task("Exercise", "Go for a 30-minute run")
    print(f"   Added task: ID {task3.id} - {task3.title}")

    print("\n2. Viewing all tasks...")
    tasks = app.service.get_all_tasks()
    table = app._format_tasks_table(tasks)
    print(table)

    print("\n3. Updating a task...")
    updated_task = app.service.update_task(1, "Buy groceries - URGENT", "Milk, bread, eggs, fruits, vegetables")
    print(f"   Updated task ID 1: {updated_task.title}")

    print("\n4. Marking a task as complete...")
    completed_task = app.service.mark_task_complete(2)
    print(f"   Marked task ID 2 as complete: {completed_task.title}")

    print("\n5. Viewing updated tasks...")
    tasks = app.service.get_all_tasks()
    table = app._format_tasks_table(tasks)
    print(table)

    print("\n6. Marking a task as incomplete...")
    incomplete_task = app.service.mark_task_incomplete(2)
    print(f"   Marked task ID 2 as incomplete: {incomplete_task.title}")

    print("\n7. Deleting a task...")
    success = app.service.delete_task(3)
    print(f"   Deleted task ID 3: {success}")

    print("\n8. Final view of tasks...")
    tasks = app.service.get_all_tasks()
    table = app._format_tasks_table(tasks)
    print(table)

    print("\n=== DEMONSTRATION COMPLETE ===")
    print("\nThe interactive menu system maintains all tasks in memory during the session.")
    print("To run the interactive application, execute: python src/cli/main.py")
    print("\nThe menu includes these options:")
    print("  1. Add Task")
    print("  2. View All Tasks")
    print("  3. Update Task")
    print("  4. Delete Task")
    print("  5. Mark Task Complete")
    print("  6. Mark Task Incomplete")
    print("  7. Exit")

if __name__ == "__main__":
    demo()