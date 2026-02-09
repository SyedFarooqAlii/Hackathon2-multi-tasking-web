"""
Custom exceptions for the todo application.
"""


class TaskNotFoundError(Exception):
    """
    Raised when a task with a specified ID is not found.
    """
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} does not exist.")


class InvalidTaskDataError(Exception):
    """
    Raised when task data is invalid.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TodoException(Exception):
    """
    Base exception class for the todo application.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)