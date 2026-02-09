from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
from uuid import UUID
import logging

# Set up logging
logger = logging.getLogger(__name__)


class TodoService:
    """
    Service class for handling todo-related business logic and database operations.
    """

    def create_todo(self, db: Session, todo: TaskCreate, user_id: UUID) -> TaskRead:
        """
        Create a new todo for the specified user.
        """
        logger.info(f"Creating new todo for user {user_id} with title: '{todo.title}'")

        db_todo = Task(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=user_id,
            category=todo.category,
            due_date=todo.due_date
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)

        logger.info(f"Successfully created todo {db_todo.id} for user {user_id}")
        return TaskRead.from_orm(db_todo) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            completed=db_todo.completed,
            user_id=db_todo.user_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at,
            category=db_todo.category,
            due_date=db_todo.due_date
        )

    def get_user_todos(self, db: Session, user_id: UUID) -> List[TaskRead]:
        """
        Get all todos for a specific user.
        """
        logger.info(f"Retrieving todos for user {user_id}")

        statement = select(Task).where(Task.user_id == user_id)
        results = db.exec(statement)
        todos = results.all()

        logger.info(f"Retrieved {len(todos)} todos for user {user_id}")
        return [TaskRead.from_orm(todo) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            category=todo.category,
            due_date=todo.due_date
        ) for todo in todos]

    def get_todo_by_id(self, db: Session, todo_id: UUID, user_id: UUID) -> Optional[TaskRead]:
        """
        Get a specific todo by ID for the specified user (ensures user ownership).
        """
        logger.info(f"Retrieving todo {todo_id} for user {user_id}")

        statement = select(Task).where(Task.id == todo_id).where(Task.user_id == user_id)
        result = db.exec(statement)
        todo = result.first()
        if todo:
            logger.info(f"Found todo {todo_id} for user {user_id}")
            return TaskRead.from_orm(todo) if hasattr(TaskRead, 'from_orm') else TaskRead(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                user_id=todo.user_id,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
        else:
            logger.info(f"Todo {todo_id} not found for user {user_id}")
            return None

    def update_todo(self, db: Session, todo_id: UUID, todo_update: TaskUpdate, user_id: UUID) -> Optional[TaskRead]:
        """
        Update a specific todo for the specified user (ensures user ownership).
        """
        logger.info(f"Updating todo {todo_id} for user {user_id}")

        statement = select(Task).where(Task.id == todo_id).where(Task.user_id == user_id)
        result = db.exec(statement)
        db_todo = result.first()
        if not db_todo:
            logger.warning(f"Attempt to update non-existent todo {todo_id} for user {user_id}")
            return None

        # Store original values for logging
        original_title = db_todo.title
        original_description = db_todo.description
        original_completed = db_todo.completed
        original_category = db_todo.category
        original_due_date = db_todo.due_date

        # Update fields that are provided
        if todo_update.title is not None:
            db_todo.title = todo_update.title
        if todo_update.description is not None:
            db_todo.description = todo_update.description
        if todo_update.completed is not None:
            db_todo.completed = todo_update.completed
        if todo_update.category is not None:
            db_todo.category = todo_update.category
        if todo_update.due_date is not None:
            db_todo.due_date = todo_update.due_date

        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)

        logger.info(f"Successfully updated todo {todo_id} for user {user_id} (title: '{original_title}' -> '{db_todo.title}', completed: {original_completed} -> {db_todo.completed})")
        return TaskRead.from_orm(db_todo) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            completed=db_todo.completed,
            user_id=db_todo.user_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at,
            category=db_todo.category,
            due_date=db_todo.due_date
        )

    def delete_todo(self, db: Session, todo_id: UUID, user_id: UUID) -> bool:
        """
        Delete a specific todo for the specified user (ensures user ownership).
        """
        logger.info(f"Deleting todo {todo_id} for user {user_id}")

        statement = select(Task).where(Task.id == todo_id).where(Task.user_id == user_id)
        result = db.exec(statement)
        db_todo = result.first()
        if not db_todo:
            logger.warning(f"Attempt to delete non-existent todo {todo_id} for user {user_id}")
            return False

        db.delete(db_todo)
        db.commit()

        logger.info(f"Successfully deleted todo {todo_id} for user {user_id}")
        return True

    def toggle_todo_completion(self, db: Session, todo_id: UUID, completed: bool, user_id: UUID) -> Optional[TaskRead]:
        """
        Toggle the completion status of a specific todo for the specified user (ensures user ownership).
        """
        logger.info(f"Toggling completion status of todo {todo_id} for user {user_id} to {completed}")

        statement = select(Task).where(Task.id == todo_id).where(Task.user_id == user_id)
        result = db.exec(statement)
        db_todo = result.first()
        if not db_todo:
            logger.warning(f"Attempt to toggle completion of non-existent todo {todo_id} for user {user_id}")
            return None

        original_completed = db_todo.completed
        db_todo.completed = completed
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)

        logger.info(f"Successfully updated completion status of todo {todo_id} for user {user_id} ({original_completed} -> {db_todo.completed})")
        return TaskRead.from_orm(db_todo) if hasattr(TaskRead, 'from_orm') else TaskRead(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            completed=db_todo.completed,
            user_id=db_todo.user_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at,
            category=db_todo.category,
            due_date=db_todo.due_date
        )


# Create a singleton instance
todo_service = TodoService()