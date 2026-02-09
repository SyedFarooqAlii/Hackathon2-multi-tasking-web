# Data Model: Todo AI Chatbot

## Entity Relationships

```
User (1) ←→ (Many) Conversation (1) ←→ (Many) Message
User (1) ←→ (Many) Task
```

## Entity Definitions

### User (Existing)
- **Entity**: User
- **Fields**:
  - `id`: String (Primary Key) - Unique user identifier
  - `email`: String - User's email address
  - `name`: String - User's display name
  - `created_at`: DateTime - Account creation timestamp
  - `updated_at`: DateTime - Last update timestamp

### Task (Existing)
- **Entity**: Task
- **Fields**:
  - `id`: Integer (Primary Key) - Auto-incrementing task ID
  - `user_id`: String (Foreign Key) - References User.id, required
  - `title`: String - Task title, required
  - `description`: String - Task description, optional
  - `completed`: Boolean - Completion status, default false
  - `created_at`: DateTime - Creation timestamp
  - `updated_at`: DateTime - Last update timestamp
- **Validation Rules**:
  - Title must be 1-255 characters
  - Description must be 0-1000 characters if provided
  - user_id must reference existing user

### Conversation (New)
- **Entity**: Conversation
- **Fields**:
  - `id`: Integer (Primary Key) - Auto-incrementing conversation ID
  - `user_id`: String (Foreign Key) - References User.id, required
  - `created_at`: DateTime - Conversation start timestamp
  - `updated_at`: DateTime - Last activity timestamp
- **Validation Rules**:
  - user_id must reference existing user
  - created_at defaults to current timestamp
  - updated_at updates automatically on changes

### Message (New)
- **Entity**: Message
- **Fields**:
  - `id`: Integer (Primary Key) - Auto-incrementing message ID
  - `conversation_id`: Integer (Foreign Key) - References Conversation.id, required
  - `role`: String - Enum('user', 'assistant'), required
  - `content`: String - Message content, required
  - `created_at`: DateTime - Message creation timestamp
- **Validation Rules**:
  - conversation_id must reference existing conversation
  - role must be either 'user' or 'assistant'
  - content must be 1-10000 characters
  - created_at defaults to current timestamp

## Database Schema

### Tables

#### conversations
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### messages
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

#### tasks (existing)
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Indexes
- conversations.user_id_idx ON conversations(user_id)
- conversations.created_at_idx ON conversations(created_at DESC)
- messages.conversation_id_idx ON messages(conversation_id)
- messages.created_at_idx ON messages(created_at ASC)
- tasks.user_id_idx ON tasks(user_id)
- tasks.completed_idx ON tasks(completed)

## Constraints
- Referential integrity between all related entities
- Prevent orphaned messages or conversations
- Enforce role values are limited to 'user' or 'assistant'

## State Transitions

### Conversation State
- Created when first message is sent in a new conversation
- Updated when new messages are added
- Remains persistent for user access across sessions

### Message State
- Immutable once created (append-only pattern)
- Timestamp records exact creation time
- Role determines message origin (user input vs AI response)

### Task State
- Created via MCP tool call when user requests to add task
- Updated via MCP tool call when user requests to modify task
- Completed via MCP tool call when user requests to complete task
- Deleted via MCP tool call when user requests to delete task