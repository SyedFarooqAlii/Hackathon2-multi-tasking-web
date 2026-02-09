from sqlmodel import SQLModel, create_engine, Session, select
from src.models.user import User
from src.core.security import get_password_hash
from src.core.config import settings
from uuid import uuid4
from datetime import datetime

# Create database engine
engine = create_engine(str(settings.database_url))

# Create tables if they don't exist
SQLModel.metadata.create_all(engine)

# Create a test user with a pre-hashed password
# Using a simple password hash for testing purposes
test_password = get_password_hash("testpassword123")

# Create user
test_user = User(
    id=uuid4(),  # Generate a new UUID
    email="test@example.com",
    hashed_password=test_password,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

# Add to database
with Session(engine) as session:
    # Check if user already exists
    statement = select(User).where(User.email == "test@example.com")
    result = session.exec(statement)
    existing_user = result.first()

    if existing_user:
        print("Test user already exists")
    else:
        session.add(test_user)
        session.commit()
        print("Test user created successfully!")

print("Test user details:")
print(f"Email: test@example.com")
print(f"Password: testpassword123")