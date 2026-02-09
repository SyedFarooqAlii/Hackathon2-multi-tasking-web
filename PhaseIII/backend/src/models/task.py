from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime
from .user import User


class TaskBase(SQLModel):
    title: str = Field(sa_column_kwargs={"nullable": False})
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    category: str = Field(default="")
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """
    Task model representing a todo item owned by a specific user.
    """
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User - commented out to prevent circular import during initialization
    # user: User = Relationship(back_populates="tasks")

    class Config:
        arbitrary_types_allowed = True


class TaskCreate(SQLModel):
    """
    Schema for creating a new task.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False
    category: str = ""
    due_date: Optional[datetime] = None
    # user_id is not included as it comes from JWT token


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    """
    Schema for reading task information.
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime