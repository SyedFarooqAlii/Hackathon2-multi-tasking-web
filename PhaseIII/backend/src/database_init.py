from sqlmodel import SQLModel
from .core.database import get_engine
from .models.user import User
from .models.task import Task
from .models.conversation import Conversation
from .models.message import Message


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    """
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_db_and_tables()