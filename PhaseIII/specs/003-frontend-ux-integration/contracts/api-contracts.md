# API Contracts: Frontend UX & API Client Integration

## Overview
This document defines the API contracts between the frontend application and the backend services for the secure multi-user todo web application.

## Authentication API

### Register User
```
POST /api/v1/users/register
```

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200)**:
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (400)**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format or password too short"
  }
}
```

**Response (409)**:
```json
{
  "error": {
    "code": "USER_EXISTS",
    "message": "User with this email already exists"
  }
}
```

### Login User
```
POST /api/v1/users/login
```

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200)**:
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer"
}
```

**Response (401)**:
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Incorrect email or password"
  }
}
```

### Get Current User
```
GET /api/v1/users/me
```

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Todo Management API

### Get User's Todos
```
GET /api/v1/users/me/tasks
```

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Todo title",
      "description": "Optional description",
      "completed": false,
      "user_id": "user-uuid",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

**Response (401)**:
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Could not validate credentials"
  }
}
```

### Create New Todo
```
POST /api/v1/users/me/tasks
```

**Headers**:
```
Authorization: Bearer {jwt-token}
Content-Type: application/json
```

**Request**:
```json
{
  "title": "New todo title",
  "description": "Optional description",
  "completed": false
}
```

**Response (200)**:
```json
{
  "id": "uuid-string",
  "title": "New todo title",
  "description": "Optional description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Get Specific Todo
```
GET /api/v1/users/me/tasks/{id}
```

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "id": "uuid-string",
  "title": "Todo title",
  "description": "Optional description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Update Todo
```
PUT /api/v1/users/me/tasks/{id}
```

**Headers**:
```
Authorization: Bearer {jwt-token}
Content-Type: application/json
```

**Request**:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200)**:
```json
{
  "id": "uuid-string",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### Delete Todo
```
DELETE /api/v1/users/me/tasks/{id}
```

**Headers**:
```
Authorization: Bearer {jwt-token}
```

**Response (200)**:
```json
{
  "message": "Task deleted successfully"
}
```

### Toggle Todo Completion
```
PATCH /api/v1/users/me/tasks/{id}/complete
```

**Headers**:
```
Authorization: Bearer {jwt-token}
Content-Type: application/json
```

**Request**:
```json
{
  "completed": true
}
```

**Response (200)**:
```json
{
  "id": "uuid-string",
  "title": "Todo title",
  "description": "Optional description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Error Response Format
All error responses follow this standard format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Optional additional details"
  }
}
```

## Common HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation error)
- **401**: Unauthorized (invalid/expired token)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **409**: Conflict (resource already exists)
- **500**: Internal Server Error

## Authentication Requirements
- All endpoints except `/users/register` and `/users/login` require a valid JWT token
- Token must be included in the `Authorization` header as `Bearer {token}`
- Tokens expire after 30 minutes (configurable)
- Refresh tokens can be used to obtain new access tokens