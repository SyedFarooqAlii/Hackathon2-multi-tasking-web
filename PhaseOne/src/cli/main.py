#!/usr/bin/env python3
"""
Interactive Console Todo Application.

This module provides an interactive menu-driven interface for the todo application.
Tasks remain in memory during the session.
"""

import os
import sys
from typing import Optional

# Add the src directory to the path so imports work properly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.todo_service import TodoService
from src.store.in_memory_store import InMemoryStore
from src.exceptions import TaskNotFoundError, InvalidTaskDataError


class InteractiveTodoApp:
    """
    Interactive menu-driven interface for the todo application.
    """

    def __init__(self):
        """
        Initialize the interactive app with a todo service.
        """
        self.service = TodoService()

    def _display_menu(self):
        """
        Display the main menu options.
        """
        print("\n" + "="*50)
        print("         INTERACTIVE TODO APPLICATION")
        print("="*50)
        print("Please select an option:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print("="*50)

    def _format_tasks_table(self, tasks) -> str:
        """
        Format tasks as a table string.

        Args:
            tasks: List of Task objects to format

        Returns:
            str: Formatted table string
        """
        if not tasks:
            return "No tasks found."

        # Create table header
        table = "\nID  | Title           | Description      | Status\n"
        table += "----|-----------------|------------------|----------\n"

        # Add each task to the table
        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            # Truncate fields to fit table if needed
            title = task.title[:15] + "..." if len(task.title) > 15 else task.title
            desc = task.description[:15] + "..." if len(task.description) > 15 else task.description
            table += f"{task.id:<3} | {title:<15} | {desc:<16} | {status}\n"

        return table

    def _add_task(self):
        """
        Handle adding a new task.
        """
        try:
            print("\n--- Add New Task ---")
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Title cannot be empty.")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            task = self.service.add_task(title, description)
            print(f"\n+ Task added successfully with ID: {task.id}")
        except ValueError as e:
            print(f"\n- Error: {str(e)}")
        except Exception as e:
            print(f"\n- Unexpected error occurred: {str(e)}")

    def _view_tasks(self):
        """
        Handle viewing all tasks.
        """
        try:
            tasks = self.service.get_all_tasks()
            table = self._format_tasks_table(tasks)
            print(table)
        except Exception as e:
            print(f"\n✗ Error retrieving tasks: {str(e)}")

    def _update_task(self):
        """
        Handle updating a task.
        """
        try:
            print("\n--- Update Task ---")
            task_id_str = input("Enter task ID to update: ").strip()

            if not task_id_str.isdigit():
                print("\n- Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)

            # Check if task exists first
            if not self.service.validate_task_id(task_id):
                print(f"\n- Error: Task with ID {task_id} does not exist.")
                return

            print(f"Current task details (ID: {task_id}):")
            current_task = self.service.get_task(task_id)
            if current_task:
                print(f"  Title: {current_task.title}")
                print(f"  Description: {current_task.description}")
                print(f"  Status: {'Complete' if current_task.completed else 'Incomplete'}")

            # Get new title (or keep current if empty input)
            new_title = input(f"\nEnter new title (current: '{current_task.title}', press Enter to keep current): ").strip()
            if not new_title:
                new_title = current_task.title

            # Get new description (or keep current if empty input)
            new_desc = input(f"Enter new description (current: '{current_task.description}', press Enter to keep current): ").strip()
            if not new_desc:
                new_desc = current_task.description

            # Update the task
            updated_task = self.service.update_task(task_id, new_title, new_desc)
            if updated_task:
                print(f"\n+ Task {task_id} updated successfully")
            else:
                print(f"\n- Error: Failed to update task {task_id}")
        except TaskNotFoundError as e:
            print(f"\n- Error: {str(e)}")
        except InvalidTaskDataError as e:
            print(f"\n- Error: {str(e)}")
        except Exception as e:
            print(f"\n- Unexpected error occurred: {str(e)}")

    def _delete_task(self):
        """
        Handle deleting a task.
        """
        try:
            print("\n--- Delete Task ---")
            task_id_str = input("Enter task ID to delete: ").strip()

            if not task_id_str.isdigit():
                print("\n- Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)

            # Check if task exists first
            if not self.service.validate_task_id(task_id):
                print(f"\n- Error: Task with ID {task_id} does not exist.")
                return

            print(f"Current task details (ID: {task_id}):")
            current_task = self.service.get_task(task_id)
            if current_task:
                print(f"  Title: {current_task.title}")
                print(f"  Description: {current_task.description}")
                print(f"  Status: {'Complete' if current_task.completed else 'Incomplete'}")

            confirm = input(f"\nAre you sure you want to delete task {task_id}? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                success = self.service.delete_task(task_id)
                if success:
                    print(f"\n+ Task {task_id} deleted successfully")
                else:
                    print(f"\n- Error: Failed to delete task {task_id}")
            else:
                print("\n- Deletion cancelled.")
        except TaskNotFoundError as e:
            print(f"\n- Error: {str(e)}")
        except Exception as e:
            print(f"\n- Unexpected error occurred: {str(e)}")

    def _mark_complete(self):
        """
        Handle marking a task as complete.
        """
        try:
            print("\n--- Mark Task Complete ---")
            task_id_str = input("Enter task ID to mark complete: ").strip()

            if not task_id_str.isdigit():
                print("\n- Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)

            # Check if task exists first
            if not self.service.validate_task_id(task_id):
                print(f"\n- Error: Task with ID {task_id} does not exist.")
                return

            # Check current status
            current_task = self.service.get_task(task_id)
            if current_task and current_task.completed:
                print(f"\n* Task {task_id} is already marked as complete.")
                return

            task = self.service.mark_task_complete(task_id)
            if task:
                print(f"\n+ Task {task_id} marked as complete")
            else:
                print(f"\n- Error: Failed to mark task {task_id} as complete")
        except TaskNotFoundError as e:
            print(f"\n- Error: {str(e)}")
        except Exception as e:
            print(f"\n- Unexpected error occurred: {str(e)}")

    def _mark_incomplete(self):
        """
        Handle marking a task as incomplete.
        """
        try:
            print("\n--- Mark Task Incomplete ---")
            task_id_str = input("Enter task ID to mark incomplete: ").strip()

            if not task_id_str.isdigit():
                print("\n- Error: Task ID must be a number.")
                return

            task_id = int(task_id_str)

            # Check if task exists first
            if not self.service.validate_task_id(task_id):
                print(f"\n- Error: Task with ID {task_id} does not exist.")
                return

            # Check current status
            current_task = self.service.get_task(task_id)
            if current_task and not current_task.completed:
                print(f"\n* Task {task_id} is already marked as incomplete.")
                return

            task = self.service.mark_task_incomplete(task_id)
            if task:
                print(f"\n+ Task {task_id} marked as incomplete")
            else:
                print(f"\n- Error: Failed to mark task {task_id} as incomplete")
        except TaskNotFoundError as e:
            print(f"\n- Error: {str(e)}")
        except Exception as e:
            print(f"\n- Unexpected error occurred: {str(e)}")

    def run(self):
        """
        Run the interactive application.
        """
        print("Welcome to the Interactive Todo Application!")
        print("Tasks will remain in memory during this session.")

        while True:
            try:
                self._display_menu()
                choice = input("\nEnter your choice (1-7): ").strip()

                if choice == '1':
                    self._add_task()
                elif choice == '2':
                    self._view_tasks()
                elif choice == '3':
                    self._update_task()
                elif choice == '4':
                    self._delete_task()
                elif choice == '5':
                    self._mark_complete()
                elif choice == '6':
                    self._mark_incomplete()
                elif choice == '7':
                    print("\nThank you for using the Todo Application! Goodbye!")
                    break
                else:
                    print("\n- Invalid choice. Please enter a number between 1 and 7.")

                # Pause to let user see the result
                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nThank you for using the Todo Application! Goodbye!")
                break
            except Exception as e:
                print(f"\n- An unexpected error occurred: {str(e)}")
                input("\nPress Enter to continue...")


def main():
    """
    Main entry point for the application.
    """
    app = InteractiveTodoApp()
    app.run()


if __name__ == "__main__":
    main()