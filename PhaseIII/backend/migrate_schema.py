#!/usr/bin/env python3
"""
Migration script to update the database schema with category and due_date columns.
This script adds the missing columns to the tasks table.
"""

import sqlite3
from pathlib import Path

def migrate_database():
    """Add category and due_date columns to the tasks table."""

    # Connect to the database
    db_path = Path(__file__).parent / "todo_app.db"
    print(f"Migrating database at: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if category column exists
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'category' not in columns:
            print("Adding category column...")
            cursor.execute("ALTER TABLE tasks ADD COLUMN category TEXT DEFAULT ''")

        if 'due_date' not in columns:
            print("Adding due_date column...")
            cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT DEFAULT NULL")

        conn.commit()
        print("Database migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()