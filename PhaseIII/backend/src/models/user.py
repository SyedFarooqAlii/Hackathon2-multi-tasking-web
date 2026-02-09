from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid
from datetime import datetime


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255, description="User's email address")


class User(UserBase, table=True):
    """
    User model representing a registered user in the system.
    """
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, description="Unique identifier for the user")
    email: str = Field(unique=True, nullable=False, max_length=255, description="User's email address")
    hashed_password: str = Field(nullable=False, description="Hashed password for authentication")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when user was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when user was last updated")


    class Config:
        arbitrary_types_allowed = True


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str

    class Config:
        # Prevent extra fields from being passed
        extra = "forbid"


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = None


class UserRead(UserBase):
    """
    Schema for reading user information (without sensitive data).
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserLogin(SQLModel):
    """
    Schema for user login credentials.
    """
    email: str
    password: str