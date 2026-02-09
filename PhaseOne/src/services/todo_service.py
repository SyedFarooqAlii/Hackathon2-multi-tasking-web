"""
Todo service layer for the todo application.

This module provides the business logic layer between the CLI interface and the in-memory store.
"""

from typing import List, Optional
from src.models.task import Task
from src.store.in_memory_store import InMemoryStore
from src.exceptions import TaskNotFoundError, InvalidTaskDataError


class TodoService:
    """
    Service layer for todo operations that handles business logic and validation.
    """

    def __init__(self, store: InMemoryStore = None):
        """
        Initialize the Todo service.

        Args:
            store (InMemoryStore, optional): The storage backend to use.
                                           If None, creates a new InMemoryStore instance.
        """
        self.store = store if store is not None else InMemoryStore()

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the todo list.

        Args:
            title (str): The title of the task (required)
            description (str): The description of the task (optional)

        Returns:
            Task: The newly created Task instance

        Raises:
            ValueError: If title validation fails
        """
        # The store handles validation through the Task constructor
        return self.store.add_task(title, description)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The Task instance if found, None if not found
        """
        return self.store.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the todo list.

        Returns:
            List[Task]: A list of all Task instances
        """
        return self.store.get_all_tasks()

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): The new title for the task
            description (str, optional): The new description for the task

        Returns:
            Task or None: The updated Task instance if successful, None if task doesn't exist

        Raises:
            InvalidTaskDataError: If the update data is invalid
            TaskNotFoundError: If the task with the given ID doesn't exist
        """
        # Check if task exists first
        if not self.validate_task_id(task_id):
            raise TaskNotFoundError(task_id)

        # Validate that at least one field is provided for update
        if title is None and description is None:
            raise InvalidTaskDataError("At least one field (title or description) must be provided for update")

        # Validate title if provided
        if title is not None and (not title or not title.strip()):
            raise InvalidTaskDataError("Title cannot be empty or only whitespace")

        result = self.store.update_task(task_id, title, description)
        if result is None:
            raise TaskNotFoundError(task_id)

        return result

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if task didn't exist
        """
        if not self.validate_task_id(task_id):
            raise TaskNotFoundError(task_id)
        return self.store.delete_task(task_id)

    def mark_task_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            Task or None: The updated Task instance if successful, None if task doesn't exist

        Raises:
            TaskNotFoundError: If the task with the given ID doesn't exist
        """
        if not self.validate_task_id(task_id):
            raise TaskNotFoundError(task_id)
        task = self.store.mark_complete(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def mark_task_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            Task or None: The updated Task instance if successful, None if task doesn't exist

        Raises:
            TaskNotFoundError: If the task with the given ID doesn't exist
        """
        if not self.validate_task_id(task_id):
            raise TaskNotFoundError(task_id)
        task = self.store.mark_incomplete(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def validate_task_id(self, task_id: int) -> bool:
        """
        Validate that a task ID exists in the store.

        Args:
            task_id (int): The ID to validate

        Returns:
            bool: True if the task exists, False otherwise
        """
        return self.store.get_task(task_id) is not None