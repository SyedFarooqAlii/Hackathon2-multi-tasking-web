"""
Task domain model for the todo application.

This module defines the Task entity with validation rules as specified in the data model.
"""

import re
from typing import Optional


class Task:
    """
    Represents a single todo item with ID, Title, Description, and Completion Status.

    Attributes:
        id (int): Unique identifier for the task, assigned sequentially starting from 1
        title (str): Descriptive name of the task, required field
        description (str): Detailed information about the task, optional field
        completed (bool): Indicates whether the task is complete or incomplete, defaults to False
    """

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            id (int): The unique identifier for the task
            title (str): The title of the task (required)
            description (str): The description of the task (optional)
            completed (bool): Whether the task is completed (defaults to False)

        Raises:
            ValueError: If validation rules are violated
        """
        self.id = self._validate_id(id)
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.completed = self._validate_completed(completed)

    def _validate_id(self, id_value: int) -> int:
        """Validate that the ID is a positive integer."""
        if not isinstance(id_value, int) or id_value <= 0:
            raise ValueError(f"ID must be a positive integer, got {id_value}")
        return id_value

    def _validate_title(self, title: str) -> str:
        """Validate that the title is not empty and within length limits."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or only whitespace")

        if len(title) > 255:
            raise ValueError(f"Title exceeds maximum length of 255 characters: {len(title)}")

        return title.strip()

    def _validate_description(self, description: str) -> str:
        """Validate that the description is within length limits."""
        if len(description) > 1000:
            raise ValueError(f"Description exceeds maximum length of 1000 characters: {len(description)}")

        return description

    def _validate_completed(self, completed: bool) -> bool:
        """Validate that completed is a boolean value."""
        if not isinstance(completed, bool):
            raise ValueError(f"Completed must be a boolean value, got {type(completed).__name__}")

        return completed

    def to_dict(self) -> dict:
        """
        Convert the Task instance to a dictionary representation.

        Returns:
            dict: Dictionary representation of the task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

    def __repr__(self) -> str:
        """
        String representation of the Task instance.

        Returns:
            str: String representation of the task
        """
        status = "Complete" if self.completed else "Incomplete"
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', status={status})"

    def __eq__(self, other) -> bool:
        """
        Compare two Task instances for equality.

        Args:
            other: Another Task instance to compare

        Returns:
            bool: True if both tasks have the same attributes, False otherwise
        """
        if not isinstance(other, Task):
            return False
        return (
            self.id == other.id and
            self.title == other.title and
            self.description == other.description and
            self.completed == other.completed
        )