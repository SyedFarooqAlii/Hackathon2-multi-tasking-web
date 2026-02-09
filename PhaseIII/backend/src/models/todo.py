from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime
from uuid import UUID


class TodoBase(SQLModel):
    title: str = Field(sa_column_kwargs={"nullable": False})
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id")


class Todo(TodoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True


class TodoCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    # Don't include id, created_at, updated_at, user_id in creation - user_id comes from the authenticated user


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoRead(TodoBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime