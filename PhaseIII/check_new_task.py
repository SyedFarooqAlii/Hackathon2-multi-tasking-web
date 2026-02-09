import psycopg2
from urllib.parse import urlparse

# Database connection string
conn_str = "postgresql://neondb_owner:npg_OSDVAB02kaRn@ep-noisy-band-ah7c3io8-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    # Connect to the database
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    print("Connected to Neon database successfully!")

    # Check for the specific new task
    cur.execute("SELECT id, title, user_id, created_at FROM tasks WHERE title = 'Final Verification Task'")
    new_tasks = cur.fetchall()

    print(f"New verification tasks found: {len(new_tasks)}")
    for task in new_tasks:
        print(f"  ID: {task[0]}")
        print(f"  Title: {task[1]}")
        print(f"  User ID: {task[2]}")
        print(f"  Created At: {task[3]}")

    # Also check for tasks created after a certain time
    cur.execute("SELECT id, title, user_id, created_at FROM tasks WHERE created_at > '2026-02-03 11:00:00' ORDER BY created_at DESC")
    recent_tasks = cur.fetchall()

    print(f"\nRecent tasks (after 11:00 AM): {len(recent_tasks)}")
    for task in recent_tasks:
        print(f"  ID: {task[0]}")
        print(f"  Title: {task[1]}")
        print(f"  User ID: {task[2]}")
        print(f"  Created At: {task[3]}")

    # Close connections
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error connecting to database: {e}")