from fastapi import APIRouter, Depends, HTTPException, status, Header, Body
from sqlmodel import Session
from typing import List
from uuid import UUID
import logging
from jose import jwt, JWTError
from pydantic import BaseModel
from src.services.todo_service import todo_service
from src.models.task import TaskCreate, TaskRead, TaskUpdate
from src.core.database import get_session
from src.core.config import settings
from src.api.deps import get_current_user_from_token

# Set up logging
logger = logging.getLogger(__name__)


class CompletionUpdate(BaseModel):
    completed: bool


router = APIRouter()


# Specific routes (must come before generic routes to ensure proper matching)


@router.get("/users/me/tasks")
def get_my_tasks(
    user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    try:
        # Get tasks for the authenticated user
        tasks = todo_service.get_user_todos(db, user_id)
        logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")
        return {"tasks": tasks}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving tasks"
        )


@router.post("/users/me/tasks", response_model=TaskRead)
def create_my_task(
    task: TaskCreate,
    user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    try:
        # Validate input
        if not task.title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title cannot be empty"
            )

        # Create the task for the authenticated user
        created_task = todo_service.create_todo(db, task, user_id)
        logger.info(f"Created task {created_task.id} for user {user_id}")
        return created_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task"
        )


@router.get("/users/me/tasks/{id}", response_model=TaskRead)
def get_my_task(
    id: UUID,
    user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Get a specific task for the authenticated user.
    """
    try:
        # Get the specific task for the authenticated user
        task = todo_service.get_todo_by_id(db, id, user_id)
        if not task:
            logger.info(f"Attempt to access non-existent task {id} by user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Retrieved task {id} for user {user_id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the task"
        )


@router.put("/users/me/tasks/{id}", response_model=TaskRead)
def update_my_task(
    id: UUID,
    task_update: TaskUpdate,
    user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    try:
        # Validate input - at least one field must be provided for update
        if not any([
            task_update.title is not None,
            task_update.description is not None,
            task_update.completed is not None,
            task_update.category is not None,
            task_update.due_date is not None
        ]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="At least one field (title, description, completed, category, or due_date) must be provided for update"
            )

        # Update the specific task for the authenticated user
        updated_task = todo_service.update_todo(db, id, task_update, user_id)
        if not updated_task:
            logger.info(f"Attempt to update non-existent task {id} by user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Updated task {id} for user {user_id}")
        return updated_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error updating task {id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the task"
        )


@router.delete("/users/me/tasks/{id}")
def delete_my_task(
    id: UUID,
    user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    try:
        # Delete the specific task for the authenticated user
        success = todo_service.delete_todo(db, id, user_id)
        if not success:
            logger.info(f"Attempt to delete non-existent task {id} by user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Deleted task {id} for user {user_id}")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error deleting task {id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the task"
        )


@router.patch("/users/me/tasks/{id}/complete", response_model=TaskRead)
def complete_my_task(
    id: UUID,
    completion_data: CompletionUpdate,
    user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Mark a specific task as complete/incomplete for the authenticated user.
    """
    try:
        # Toggle the completion status of the specific task for the authenticated user
        updated_task = todo_service.toggle_todo_completion(db, id, completion_data.completed, user_id)
        if not updated_task:
            logger.info(f"Attempt to update non-existent task {id} by user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Updated completion status of task {id} for user {user_id} to {completion_data.completed}")
        return updated_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error updating completion status of task {id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the task completion status"
        )


# Generic routes (must come after specific routes to avoid intercepting specific route requests)


@router.get("/users/{user_id}/tasks")
def get_user_tasks(
    user_id: str,
    current_user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Get all tasks for a specific user (with verification against JWT token).
    Note: user_id in path is for API contract, but we verify against JWT token.
    """
    try:
        # Check if user_id is "me" - if so, this should have matched the /users/me/tasks route instead
        if user_id.lower() == "me":
            logger.warning(f"Request to /users/me/tasks was caught by /users/{{user_id}}/tasks route")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid user ID format"
            )

        # Convert string user_id to UUID
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            logger.warning(f"Invalid UUID format: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid user ID format"
            )

        # Verify that the user_id in the path matches the authenticated user from JWT
        if user_uuid != current_user_id:
            logger.warning(f"User {current_user_id} attempted to access tasks for user {user_uuid}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot access another user's tasks"
            )

        # Get tasks for the authenticated user
        tasks = todo_service.get_user_todos(db, current_user_id)
        logger.info(f"Retrieved {len(tasks)} tasks for user {current_user_id}")
        return {"tasks": tasks}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving tasks"
        )


@router.post("/users/{user_id}/tasks", response_model=TaskRead)
def create_user_task(
    user_id: str,
    task: TaskCreate,
    current_user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    Note: user_id in path is for API contract, but we verify against JWT token.
    """
    try:
        # Verify that the user_id in the path matches the authenticated user from JWT
        if user_id != current_user_id:
            logger.warning(f"User {current_user_id} attempted to create task for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot create tasks for another user"
            )

        # Validate input
        if not task.title.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title cannot be empty"
            )

        # Create the task for the authenticated user
        created_task = todo_service.create_todo(db, task, current_user_id)
        logger.info(f"Created task {created_task.id} for user {current_user_id}")
        return created_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error creating task for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task"
        )


@router.get("/users/{user_id}/tasks/{id}", response_model=TaskRead)
def get_user_task(
    user_id: str,
    id: UUID,
    current_user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Get a specific task for the authenticated user.
    Note: user_id in path is for API contract, but we verify against JWT token.
    """
    try:
        # Verify that the user_id in the path matches the authenticated user from JWT
        if user_id != current_user_id:
            logger.warning(f"User {current_user_id} attempted to access task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot access another user's tasks"
            )

        # Get the specific task for the authenticated user
        task = todo_service.get_todo_by_id(db, id, current_user_id)
        if not task:
            logger.info(f"Attempt to access non-existent task {id} by user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Retrieved task {id} for user {current_user_id}")
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {id} for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the task"
        )


@router.put("/users/{user_id}/tasks/{id}", response_model=TaskRead)
def update_user_task(
    user_id: str,
    id: UUID,
    task_update: TaskUpdate,
    current_user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    Note: user_id in path is for API contract, but we verify against JWT token.
    """
    try:
        # Verify that the user_id in the path matches the authenticated user from JWT
        if user_id != current_user_id:
            logger.warning(f"User {current_user_id} attempted to update task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot update another user's tasks"
            )

        # Validate input - at least one field must be provided for update
        if not any([
            task_update.title is not None,
            task_update.description is not None,
            task_update.completed is not None,
            task_update.category is not None,
            task_update.due_date is not None
        ]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="At least one field (title, description, completed, category, or due_date) must be provided for update"
            )

        # Update the specific task for the authenticated user
        updated_task = todo_service.update_todo(db, id, task_update, current_user_id)
        if not updated_task:
            logger.info(f"Attempt to update non-existent task {id} by user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Updated task {id} for user {current_user_id}")
        return updated_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error updating task {id} for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the task"
        )


@router.delete("/users/{user_id}/tasks/{id}")
def delete_user_task(
    user_id: str,
    id: UUID,
    current_user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    Note: user_id in path is for API contract, but we verify against JWT token.
    """
    try:
        # Verify that the user_id in the path matches the authenticated user from JWT
        if user_id != current_user_id:
            logger.warning(f"User {current_user_id} attempted to delete task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot delete another user's tasks"
            )

        # Delete the specific task for the authenticated user
        success = todo_service.delete_todo(db, id, current_user_id)
        if not success:
            logger.info(f"Attempt to delete non-existent task {id} by user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Deleted task {id} for user {current_user_id}")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error deleting task {id} for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the task"
        )


@router.patch("/users/{user_id}/tasks/{id}/complete", response_model=TaskRead)
def complete_user_task(
    user_id: str,
    id: UUID,
    completion_data: CompletionUpdate,
    current_user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Mark a specific task as complete/incomplete for the authenticated user.
    Note: user_id in path is for API contract, but we verify against JWT token.
    """
    try:
        # Verify that the user_id in the path matches the authenticated user from JWT
        if user_id != current_user_id:
            logger.warning(f"User {current_user_id} attempted to update task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot update another user's tasks"
            )

        # Toggle the completion status of the specific task for the authenticated user
        updated_task = todo_service.toggle_todo_completion(db, id, completion_data.completed, current_user_id)
        if not updated_task:
            logger.info(f"Attempt to update non-existent task {id} by user {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        logger.info(f"Updated completion status of task {id} for user {current_user_id} to {completion_data.completed}")
        return updated_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error updating completion status of task {id} for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the task completion status"
        )