from typing import Dict, Any, Optional
from sqlmodel import Session
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from sqlalchemy.exc import IntegrityError
from ..core.errors import TaskNotFoundError, AuthorizationError
import uuid


class MCPTaskService:
    """
    Service class implementing MCP-style task operations
    These are designed to be called as tools by the AI agent
    """

    def __init__(self):
        pass

    def add_task(self, db_session: Session, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP tool: Add a new task for a user
        """
        try:
            # Create a new task
            task_data = TaskCreate(
                title=title,
                description=description or "",
                user_id=uuid.UUID(user_id) if isinstance(user_id, str) and len(user_id) == 36 else user_id
            )

            # Convert to proper Task model instance
            task = Task(
                title=task_data.title,
                description=task_data.description,
                user_id=task_data.user_id if hasattr(task_data, 'user_id') else uuid.UUID(user_id)
            )

            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)

            return {
                "success": True,
                "message": f"Task '{task.title}' added successfully",
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
            }
        except Exception as e:
            db_session.rollback()
            return {
                "success": False,
                "error": str(e)
            }

    def list_tasks(self, db_session: Session, user_id: str, status: Optional[str] = "all") -> Dict[str, Any]:
        """
        MCP tool: List tasks for a user
        """
        try:
            # Query tasks for the specific user
            query = db_session.query(Task).filter(Task.user_id == uuid.UUID(user_id))

            # Apply status filter if specified
            if status == "active":
                query = query.filter(Task.completed == False)
            elif status == "completed":
                query = query.filter(Task.completed == True)
            # If status is "all" or any other value, return all tasks

            tasks = query.all()

            return {
                "success": True,
                "tasks": [
                    {
                        "id": str(task.id),
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None
                    }
                    for task in tasks
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_task(self, db_session: Session, user_id: str, task_id: str,
                   title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP tool: Update an existing task for a user
        """
        try:
            # Find the task and verify it belongs to the user
            task_uuid = uuid.UUID(task_id) if len(task_id) == 36 else task_id
            user_uuid = uuid.UUID(user_id) if len(user_id) == 36 else user_id

            task = db_session.query(Task).filter(
                Task.id == task_uuid,
                Task.user_id == user_uuid
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task with id {task_id} not found or does not belong to user"
                }

            # Update the task fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)

            return {
                "success": True,
                "message": f"Task '{task.id}' updated successfully",
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
            }
        except Exception as e:
            db_session.rollback()
            return {
                "success": False,
                "error": str(e)
            }

    def complete_task(self, db_session: Session, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        MCP tool: Mark a task as completed for a user
        """
        try:
            # Find the task and verify it belongs to the user
            task_uuid = uuid.UUID(task_id) if len(task_id) == 36 else task_id
            user_uuid = uuid.UUID(user_id) if len(user_id) == 36 else user_id

            task = db_session.query(Task).filter(
                Task.id == task_uuid,
                Task.user_id == user_uuid
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task with id {task_id} not found or does not belong to user"
                }

            # Mark the task as completed
            task.completed = True
            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)

            return {
                "success": True,
                "message": f"Task '{task.id}' marked as completed",
                "task": {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
            }
        except Exception as e:
            db_session.rollback()
            return {
                "success": False,
                "error": str(e)
            }

    def delete_task(self, db_session: Session, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        MCP tool: Delete a task for a user
        """
        try:
            # Find the task and verify it belongs to the user
            task_uuid = uuid.UUID(task_id) if len(task_id) == 36 else task_id
            user_uuid = uuid.UUID(user_id) if len(user_id) == 36 else user_id

            task = db_session.query(Task).filter(
                Task.id == task_uuid,
                Task.user_id == user_uuid
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task with id {task_id} not found or does not belong to user"
                }

            # Delete the task
            db_session.delete(task)
            db_session.commit()

            return {
                "success": True,
                "message": f"Task '{task.id}' deleted successfully"
            }
        except Exception as e:
            db_session.rollback()
            return {
                "success": False,
                "error": str(e)
            }


# Global instance of the MCP task service
mcp_task_service = MCPTaskService()