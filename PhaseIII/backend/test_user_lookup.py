#!/usr/bin/env python3
"""Test script to verify user lookup functionality."""

from sqlmodel import SQLModel, create_engine, Session, select
from uuid import UUID
from src.models.user import User
from src.core.database import engine

# Test user ID from the database
user_id_str = "c95e2c1c-4edc-4268-ae58-ae6dd4aab914"
user_id = UUID(user_id_str)

print(f"Testing user lookup for ID: {user_id}")

# Try to get the user using SQLModel
with Session(engine) as session:
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement)
    user = result.first()

    if user:
        print(f"✅ User found: {user.email}")
        print(f"   ID: {user.id}")
        print(f"   Hashed password: {user.hashed_password[:20]}..." if user.hashed_password else "No password")
    else:
        print("❌ User NOT found using SQLModel")

        # Try a broader query to see what's in the DB
        all_users = session.exec(select(User)).all()
        print(f"\nTotal users in session: {len(all_users)}")
        for u in all_users:
            print(f"  - ID: {u.id}, Email: {u.email}")