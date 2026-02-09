import sqlite3
import psycopg2
from urllib.parse import urlparse
import uuid
from datetime import datetime

# Connect to SQLite database
sqlite_conn = sqlite3.connect(r'C:\Users\PMLS\Desktop\hackathon2_phase1\PhaseII\backend\todo_app.db')
sqlite_cursor = sqlite_conn.cursor()

# Connect to Neon PostgreSQL database
neon_conn_str = "postgresql://neondb_owner:npg_OSDVAB02kaRn@ep-noisy-band-ah7c3io8-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
neon_conn = psycopg2.connect(neon_conn_str)
neon_cursor = neon_conn.cursor()

print("Connected to both databases successfully!")

# Copy users from SQLite to Neon
print("Copying users...")
sqlite_cursor.execute("SELECT id, email, hashed_password, created_at, updated_at FROM users")
sqlite_users = sqlite_cursor.fetchall()

for user in sqlite_users:
    user_id, email, hashed_password, created_at, updated_at = user

    # Format datetime if it's a string
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    if isinstance(updated_at, str):
        updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))

    try:
        neon_cursor.execute("""
            INSERT INTO users (id, email, hashed_password, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (str(user_id), email, hashed_password, created_at, updated_at))
    except Exception as e:
        print(f"Error inserting user {user_id}: {e}")

# Copy tasks from SQLite to Neon
print("Copying tasks...")
sqlite_cursor.execute("SELECT id, title, description, completed, user_id, created_at, updated_at FROM tasks")
sqlite_tasks = sqlite_cursor.fetchall()

for task in sqlite_tasks:
    id, title, description, completed, user_id, created_at, updated_at = task

    # Format datetime if it's a string
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    if isinstance(updated_at, str):
        updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))

    try:
        # Convert SQLite integer boolean to PostgreSQL boolean
        completed_bool = bool(completed)
        neon_cursor.execute("""
            INSERT INTO tasks (id, title, description, completed, user_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (id, title, description, completed_bool, user_id, created_at, updated_at))
    except Exception as e:
        print(f"Error inserting task {id}: {e}")

# Commit changes to Neon
neon_conn.commit()

# Verify the copy
neon_cursor.execute("SELECT COUNT(*) FROM users")
neon_user_count = neon_cursor.fetchone()[0]
neon_cursor.execute("SELECT COUNT(*) FROM tasks")
neon_task_count = neon_cursor.fetchone()[0]

print(f"Verification:")
print(f"- Users in Neon DB: {neon_user_count}")
print(f"- Tasks in Neon DB: {neon_task_count}")

# Close connections
sqlite_conn.close()
neon_conn.close()

print("Data migration completed!")