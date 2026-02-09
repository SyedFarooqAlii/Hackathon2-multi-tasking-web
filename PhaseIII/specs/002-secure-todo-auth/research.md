# Research: Secure Multi-User Todo Web App with JWT Authentication (Spec2)

**Feature**: 002-secure-todo-auth | **Date**: 2026-01-19

## Research Summary

This document captures the research findings for implementing the secure multi-user todo web application with JWT-based authentication, focusing on technology decisions and best practices as specified in the updated requirements.

## Decision: JWT Verification Method in FastAPI (Middleware vs Dependency)

**Decision**: Use dependency injection approach for JWT verification
**Rationale**:
- Provides more granular control over authentication requirements per endpoint
- Easier to implement role-based access controls if needed later
- Better integration with FastAPI's dependency injection system
- More flexible than global middleware for selective protection
- Enables easy testing with different authentication scenarios
**Alternatives considered**:
- Middleware approach: Would apply authentication globally, less flexible
- Decorator pattern: Less integrated with FastAPI's native approach

## Decision: Token Expiry Handling Strategy

**Decision**: Implement short-lived access tokens (30 minutes) with refresh token mechanism
**Rationale**:
- Enhanced security through limited token lifespan
- Reduces impact if tokens are compromised
- Balances security with user experience
- Follows industry best practices for JWT implementations
- Forces regular re-authentication for sensitive operations
**Implementation approach**:
- Access tokens: 30 minutes expiry
- Refresh tokens: 7 days expiry (stored securely)
- Frontend automatically refreshes tokens before expiry
- Clear token rotation strategy

## Decision: API Error Response Standards

**Decision**: Implement consistent error response format with standardized HTTP status codes
**Rationale**:
- Consistent error handling across frontend and backend
- Clear communication of error types to clients
- Standardized format simplifies frontend error handling
- Better debugging and monitoring capabilities
- Follows REST API best practices
**Response format**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details (optional)"
  }
}
```

## Decision: SQLModel Relationship Design (User → Tasks)

**Decision**: Implement one-to-many relationship with foreign key constraint and cascade deletion
**Rationale**:
- Enforces data integrity at database level
- Ensures tasks are automatically cleaned up when users are deleted
- Enables efficient querying with JOINs
- Prevents orphaned records in the database
- Supports the business requirement of user data isolation
**Implementation**:
- User.id as primary key
- Task.user_id as foreign key referencing User.id
- Cascade delete on user removal
- Index on user_id for efficient filtering

## Decision: Frontend API Client Abstraction

**Decision**: Create centralized API client with built-in JWT token management
**Rationale**:
- Centralizes authentication logic in one place
- Simplifies API calls throughout the application
- Automatic token attachment to requests
- Consistent error handling across all API calls
- Easy to mock for testing purposes
**Features**:
- Automatic JWT token inclusion in headers
- Token refresh on expiration
- Consistent error handling
- Request/response interceptors
- Type-safe API calls

## Architecture Research: Auth-Aware Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Better       │    │   FastAPI       │
│   (Next.js)     │───▶│     Auth        │───▶│   Backend       │
│                 │    │                 │    │                 │
│ - Login/Signup  │    │ - User          │    │ - JWT           │
│ - Token Storage │    │   Registration  │    │   Verification  │
│ - API Calls     │    │ - Session       │    │ - User          │
│                 │    │   Management    │    │   Validation    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                            ┌─────────────────────────┐
                                            │      Neon PostgreSQL    │
                                            │                         │
                                            │ - Users table           │
                                            │ - Tasks table           │
                                            │ - User-Task relationship│
                                            └─────────────────────────┘
```

## Interaction Flow Research: Frontend → Auth → API → DB

1. **User Action**: User attempts to register/login on frontend
2. **Auth Layer**: Better Auth handles registration/login and issues JWT
3. **Frontend Storage**: Token securely stored (httpOnly cookie or secure local storage)
4. **API Request**: Frontend makes API call with Authorization: Bearer <token>
5. **Token Verification**: FastAPI extracts and verifies JWT signature
6. **User Validation**: Backend confirms user identity from token claims
7. **Database Query**: Backend queries database with user-specific filters
8. **Response**: Data returned respecting user isolation constraints

## Agent Responsibility Mapping Research

### Auth Agent Responsibilities:
- User registration and login flows
- JWT token generation and validation
- Password hashing and security
- Session management (if needed)

### Frontend Agent Responsibilities:
- UI components for authentication
- Secure token storage and management
- API client implementation
- User experience and feedback

### Backend Agent Responsibilities:
- API endpoint implementation
- JWT verification middleware/dependencies
- Business logic implementation
- Database interaction and validation

### DB Agent Responsibilities:
- Schema design and relationships
- Data integrity constraints
- User isolation enforcement
- Migration management

## Data Model Research: User-Task Ownership Constraints

### Primary Constraints:
- Foreign key constraint: Task.user_id → User.id
- Cascade delete: User deletion removes associated tasks
- Unique indexes: Efficient querying by user_id
- Not-null constraints: Required fields enforcement

### Security Constraints:
- Row-level security: Users can only access their own tasks
- Parameter validation: Prevent user_id manipulation
- Authorization checks: Verify JWT matches requested user

### Performance Constraints:
- Index optimization: Fast user-based queries
- Connection pooling: Efficient database connections
- Query optimization: Minimize database round trips