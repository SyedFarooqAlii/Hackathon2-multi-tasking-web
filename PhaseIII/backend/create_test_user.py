#!/usr/bin/env python3
"""
Script to create a test user in the database with a SHA-256 hashed password
to work around the bcrypt environment issue.
"""

import sqlite3
import uuid
from datetime import datetime
import hashlib

# Connect to the SQLite database
conn = sqlite3.connect('todo_app.db')
cursor = conn.cursor()

# Create a test user with a SHA-256 hashed password
email = "admin@example.com"
password = "admin123"

# Create a SHA-256 hash of the password
password_hash = hashlib.sha256(password.encode()).hexdigest()
hashed_password = f"sha256:{password_hash}"  # Add prefix to identify as SHA-256 hash

# Generate a UUID for the user
user_id = str(uuid.uuid4())

# Insert the test user into the database
try:
    cursor.execute("""
        INSERT INTO users (id, email, hashed_password, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        email,
        hashed_password,
        datetime.utcnow(),
        datetime.utcnow()
    ))

    conn.commit()
    print(f"Test user created successfully!")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"User ID: {user_id}")
    print("\nYou can now log in with these credentials.")

except sqlite3.IntegrityError:
    print(f"Test user {email} already exists in the database.")
    # Update the existing user with the new password hash
    cursor.execute("""
        UPDATE users
        SET hashed_password = ?
        WHERE email = ?
    """, (hashed_password, email))

    conn.commit()
    print(f"Updated existing user {email} with new password hash.")

conn.close()
print("\nThe backend server needs to be restarted to pick up the security changes.")