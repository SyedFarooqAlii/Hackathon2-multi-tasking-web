"""
In-memory store for the todo application.

This module implements a dictionary-based storage system for tasks with O(1) lookup times.
"""

from typing import Dict, List, Optional
from src.models.task import Task


class InMemoryStore:
    """
    Dictionary-based in-memory storage for tasks.

    The store uses integer keys (task IDs) to map to Task objects for O(1) access.
    """

    def __init__(self):
        """
        Initialize the in-memory store with an empty dictionary.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the store with a unique ID.

        Args:
            title (str): The title of the task
            description (str): The description of the task (optional)

        Returns:
            Task: The newly created Task instance with assigned ID

        Raises:
            ValueError: If title validation fails in Task constructor
        """
        # Create a new task with the next available ID
        new_task = Task(id=self._next_id, title=title, description=description, completed=False)
        self._tasks[new_task.id] = new_task
        self._next_id += 1
        return new_task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The Task instance if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the store.

        Returns:
            List[Task]: A list of all Task instances, sorted by ID
        """
        # Return tasks sorted by ID to ensure consistent ordering
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): The new title for the task
            description (str, optional): The new description for the task

        Returns:
            Task or None: The updated Task instance if found, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]

        # Update fields if they are provided
        if title is not None:
            # Create a new task instance to trigger validation
            updated_task = Task(
                id=task.id,
                title=title,
                description=task.description if description is None else description,
                completed=task.completed
            )
        elif description is not None:
            updated_task = Task(
                id=task.id,
                title=task.title,
                description=description,
                completed=task.completed
            )
        else:
            # No changes provided, return the existing task
            return task

        # Update the stored task
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if task didn't exist
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            Task or None: The updated Task instance if found, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=True
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            Task or None: The updated Task instance if found, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=False
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            int: The next available ID
        """
        return self._next_id

    def clear_all(self) -> None:
        """
        Clear all tasks from the store. This is primarily for testing purposes.
        """
        self._tasks.clear()
        self._next_id = 1