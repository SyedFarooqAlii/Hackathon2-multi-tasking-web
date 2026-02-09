# Quickstart Guide: Authenticated Full-Stack Todo Web Application

**Feature**: 001-auth-fullstack-todo | **Date**: 2026-01-16

## Overview

This guide provides instructions for setting up and running the authenticated full-stack todo web application with JWT-based authentication.

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Better Auth compatible environment
- Environment variables configured

## Environment Setup

### Backend Configuration

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://username:password@host:port/database_name
NEON_DATABASE_URL=postgresql://your-neon-connection-string
SECRET_KEY=your-super-secret-jwt-signing-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Configuration

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Installation Steps

### 1. Backend Setup

```bash
cd backend
pip install fastapi sqlmodel uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] psycopg2-binary python-dotenv
```

### 2. Frontend Setup

```bash
cd frontend
npm install next react react-dom @types/react @types/node
npm install better-auth @better-auth/react
```

### 3. Database Setup

Initialize the database with the required schema:

```bash
# Run database migrations
python -m backend.src.core.database --setup
```

## Running the Application

### Backend

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## API Usage

### Authentication Flow

1. **Register a user**:
   ```bash
   POST /api/v1/users/register
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "securePassword123"
   }
   ```

2. **Login to get JWT token**:
   ```bash
   POST /api/v1/users/login
   Content-Type: application/json

   {
     "email": "user@example.com",
     "password": "securePassword123"
   }
   ```

   Response:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIs...",
     "token_type": "bearer"
   }
   ```

3. **Use JWT token for authenticated requests**:
   ```bash
   GET /api/v1/users/me
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
   ```

### Todo Operations

#### Get user's todos:
```bash
GET /api/v1/users/{user_id}/tasks
Authorization: Bearer <jwt_token>
```

#### Create a new todo:
```bash
POST /api/v1/users/{user_id}/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, bread, eggs"
}
```

#### Update a todo:
```bash
PUT /api/v1/users/{user_id}/tasks/{task_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Buy groceries (updated)",
  "description": "Milk, bread, eggs, fruits",
  "completed": false
}
```

#### Delete a todo:
```bash
DELETE /api/v1/users/{user_id}/tasks/{task_id}
Authorization: Bearer <jwt_token>
```

#### Mark todo as complete:
```bash
PATCH /api/v1/users/{user_id}/tasks/{task_id}/complete
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "completed": true
}
```

## Testing the Application

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Security Notes

1. **JWT Verification**: All API endpoints verify JWT tokens before processing requests
2. **User ID Verification**: User ID is always derived from JWT token, never from request path
3. **Data Isolation**: Users can only access their own data
4. **Environment Variables**: Keep secrets in environment variables, never in code

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure your database URL is correctly configured
2. **JWT Expiration**: Tokens expire after 30 minutes by default; implement refresh logic
3. **CORS Issues**: Configure CORS settings in the backend for frontend communication
4. **Authentication Failures**: Verify that Better Auth is properly configured

### Debugging Tips

1. Check server logs for detailed error messages
2. Verify JWT token format and validity
3. Ensure all environment variables are properly set
4. Confirm database connectivity and schema integrity