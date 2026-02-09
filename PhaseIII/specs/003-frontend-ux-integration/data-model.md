# Data Model: Frontend UX & API Client Integration

## Entity: User
**Description**: Represents a registered user in the system

**Fields**:
- `id`: string (UUID) - Unique identifier for the user
- `email`: string (required, unique) - User's email address
- `created_at`: DateTime - Timestamp when user was created
- `updated_at`: DateTime - Timestamp when user was last updated

**Validations**:
- Email must be in valid email format
- Email must be unique across all users
- Email is required during registration

**Relationships**:
- One-to-many with Todo entities (one user can have many todos)

## Entity: Todo
**Description**: Represents a todo item owned by a specific user

**Fields**:
- `id`: string (UUID) - Unique identifier for the todo
- `title`: string (required, max 255 chars) - Title of the todo
- `description`: string (optional) - Additional details about the todo
- `completed`: boolean (default: false) - Whether the todo is completed
- `user_id`: string (required, foreign key) - Reference to the owning user
- `created_at`: DateTime - Timestamp when todo was created
- `updated_at`: DateTime - Timestamp when todo was last updated

**Validations**:
- Title is required and cannot be empty
- Title must be less than 255 characters
- Description is optional
- Completed defaults to false if not provided
- user_id must reference a valid user

**Relationships**:
- Many-to-one with User entity (many todos belong to one user)

## Entity: AuthToken
**Description**: Represents a JWT authentication token

**Fields**:
- `access_token`: string (required) - The JWT token string
- `token_type`: string (default: "bearer") - Type of token
- `expires_in`: number (optional) - Expiration time in seconds
- `refresh_token`: string (optional) - Refresh token if applicable

**Validations**:
- access_token is required
- token_type defaults to "bearer" if not provided

**Relationships**:
- Associated with User entity during authentication

## State Transitions

### Todo State Transitions
- **Incomplete → Complete**: User toggles completion status
- **Complete → Incomplete**: User unchecks completion status
- **Active → Deleted**: User deletes the todo (soft delete)

### Auth State Transitions
- **Unauthenticated → Authenticating**: User submits login credentials
- **Authenticating → Authenticated**: Login successful with valid token
- **Authenticating → Unauthenticated**: Login failed
- **Authenticated → Unauthenticated**: Token expires or user logs out

## API Response Structures

### User Response
```typescript
interface UserResponse {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}
```

### Todo Response
```typescript
interface TodoResponse {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}
```

### Auth Response
```typescript
interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in?: number;
  refresh_token?: string;
}
```

### Error Response
```typescript
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}
```

## Frontend State Model

### Application State
```typescript
interface AppState {
  auth: {
    user: UserResponse | null;
    token: string | null;
    loading: boolean;
    error: string | null;
  };
  todos: {
    items: TodoResponse[];
    loading: boolean;
    error: string | null;
    selectedTodo: TodoResponse | null;
  };
}
```

### Form State
```typescript
interface TodoFormState {
  title: string;
  description: string;
  completed: boolean;
  errors: {
    title?: string;
    description?: string;
  };
  submitting: boolean;
}
```

This data model provides the foundation for the frontend application's data handling and ensures consistency between the frontend and backend systems.