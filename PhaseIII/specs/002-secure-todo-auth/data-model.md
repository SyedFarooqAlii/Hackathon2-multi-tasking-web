# Data Model: Secure Multi-User Todo Web App with JWT Authentication (Spec2)

**Feature**: 002-secure-todo-auth | **Date**: 2026-01-19

## Overview

This document defines the data models for the secure multi-user todo application, focusing on user authentication and task management with strict data isolation between users. The model incorporates user-task ownership constraints and security considerations.

## Entity Definitions

### User Entity

**Purpose**: Represents a registered user in the system with authentication credentials managed by Better Auth

**Fields**:
- `id`: UUID (Primary Key)
  - Unique identifier for the user
  - Auto-generated using UUID4
  - Immutable after creation
- `email`: String (Required, Unique, Indexed)
  - User's email address for identification
  - Validated as proper email format
  - Used for login and communication
- `hashed_password`: String (Required)
  - Securely hashed password for authentication
  - Stored using bcrypt or similar secure hashing
- `created_at`: DateTime (Required)
  - Timestamp when user account was created
  - Auto-set on creation
  - UTC timezone
- `updated_at`: DateTime (Required)
  - Timestamp when user record was last modified
  - Auto-updated on changes
  - UTC timezone

**Relationships**:
- One-to-Many: User → Tasks (user owns many tasks)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Email cannot be changed after account creation
- Password must meet security requirements

### Task Entity

**Purpose**: Represents a task item owned by a specific user with status tracking

**Fields**:
- `id`: UUID (Primary Key)
  - Unique identifier for the task item
  - Auto-generated using UUID4
  - Immutable after creation
- `title`: String (Required, Max 255 chars)
  - Title or subject of the task
  - Displayed in lists and views
- `description`: String (Optional, Max 1000 chars)
  - Detailed description of the task
  - May contain rich text or formatting
- `completed`: Boolean (Required, Default: false)
  - Status indicating if the task is completed
  - Used for filtering and display
- `user_id`: UUID (Foreign Key, Required)
  - Reference to the owner user
  - Enforces data ownership and isolation
  - Links to User.id
- `created_at`: DateTime (Required)
  - Timestamp when task was created
  - Auto-set on creation
  - UTC timezone
- `updated_at`: DateTime (Required)
  - Timestamp when task was last modified
  - Auto-updated on changes
  - UTC timezone

**Relationships**:
- Many-to-One: Task → User (task belongs to one user)

**Validation Rules**:
- Title must not be empty
- User_id must reference an existing user
- Completed status can be toggled by the owner
- Only the owner can modify the task

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for email lookup
CREATE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for user-based queries (critical for data isolation)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for completed status (common query pattern)
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## Access Control Rules

### Read Access
- Users can only read their own tasks
- Backend must verify JWT token and match user_id
- Queries must filter by authenticated user's ID

### Write Access
- Users can only modify their own tasks
- Operations (UPDATE, DELETE) must verify ownership
- Prevent modification of other users' tasks

### Create Access
- Users can only create tasks for themselves
- Backend must derive user_id from JWT token
- Never trust user_id from request parameters

## State Transitions

### Task Completion
- `completed = false` → `completed = true` (when user marks as complete)
- `completed = true` → `completed = false` (when user unmarks as complete)

### Data Lifecycle
- New task: `created_at` set, `completed = false`
- Updated task: `updated_at` refreshed
- Deleted task: Automatically removed due to CASCADE constraint

## Constraints for Data Integrity

1. **Referential Integrity**: Foreign key constraint ensures tasks reference valid users
2. **Data Isolation**: Index on user_id enables efficient filtering by ownership
3. **Cascade Deletion**: When user is deleted, their tasks are automatically removed
4. **Required Fields**: Essential fields cannot be null
5. **Unique Constraints**: Email uniqueness prevents duplicate accounts

## Query Patterns

### Common Queries
1. Get all tasks for authenticated user: `SELECT * FROM tasks WHERE user_id = ?`
2. Get completed tasks for user: `SELECT * FROM tasks WHERE user_id = ? AND completed = TRUE`
3. Get specific task by ID and user: `SELECT * FROM tasks WHERE id = ? AND user_id = ?`

### Performance Considerations
- Index on user_id critical for data isolation queries
- Index on completed status for filtering completed tasks
- UUID primary keys provide security through opacity