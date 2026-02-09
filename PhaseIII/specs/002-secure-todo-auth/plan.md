# Implementation Plan: Secure Multi-User Todo Web App with JWT Authentication (Spec2)

**Branch**: `002-secure-todo-auth` | **Date**: 2026-01-19 | **Spec**: ../spec.md
**Input**: Feature specification from `/specs/002-secure-todo-auth/spec.md`

## Summary

Design and implement a secure, multi-user todo web application with JWT-based authentication using Better Auth, Next.js frontend, FastAPI backend, and Neon PostgreSQL database. The system will enforce strict user data isolation and follow a stateless authentication architecture with refined auth-aware architecture and comprehensive testing strategy.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript for Next.js 16+, Node.js 18+
**Primary Dependencies**: Next.js 16+ (App Router), FastAPI, SQLModel, Neon PostgreSQL, Better Auth
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest for backend, Jest/Vitest for frontend, Playwright for E2E
**Target Platform**: Web application with responsive design
**Project Type**: Full-stack web application with separate frontend/backend
**Performance Goals**: Sub-500ms API response times, 95% uptime, concurrent user support
**Constraints**: JWT-based auth, user data isolation, security-first design
**Scale/Scope**: Multi-user support with data isolation, persistent storage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-driven development: All implementation follows written specs
- ✅ Security-first authentication: JWT-based auth with user isolation
- ✅ Clear separation of concerns: Frontend/Backend/Database/Auth layers
- ✅ Deterministic agent workflow: Using Claude Code + Spec-Kit Plus
- ✅ User data isolation: Each user can only access their own tasks

## Project Structure

### Documentation (this feature)
```text
specs/002-secure-todo-auth/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── tasks.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   └── main.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   ├── register/
│   │   └── tasks/
│   ├── components/
│   │   ├── auth/
│   │   ├── tasks/
│   │   └── ui/
│   ├── lib/
│   │   ├── auth.ts
│   │   ├── api.ts
│   │   └── types.ts
│   └── styles/
├── public/
└── tests/
    ├── unit/
    └── e2e/
```

**Structure Decision**: Selected the Web application structure with separate frontend/backend to maintain clear separation of concerns between client-side UI and server-side business logic.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | None       | None                                |

## Phase 0: Research & Decision Points

### Decision 1: JWT verification method in FastAPI (middleware vs dependency)

**Decision**: Use dependency injection approach for JWT verification
**Rationale**: Provides more granular control over authentication requirements per endpoint, easier to implement role-based access controls if needed later, better integration with FastAPI's dependency injection system, and more flexible than global middleware for selective protection.
**Alternatives considered**: Global middleware approach, decorator pattern

### Decision 2: Token expiry handling strategy

**Decision**: Implement short-lived access tokens (30 minutes) with refresh token mechanism
**Rationale**: Enhanced security through limited token lifespan, reduces impact if tokens are compromised, balances security with user experience, follows industry best practices for JWT implementations, forces regular re-authentication for sensitive operations.
**Implementation approach**: Access tokens: 30 minutes expiry, Refresh tokens: 7 days expiry (stored securely), Frontend automatically refreshes tokens before expiry, Clear token rotation strategy.

### Decision 3: API error response standards

**Decision**: Implement consistent error response format with standardized HTTP status codes
**Rationale**: Consistent error handling across frontend and backend, clear communication of error types to clients, standardized format simplifies frontend error handling, better debugging and monitoring capabilities, follows REST API best practices.
**Response format**: Standardized JSON error format with code, message, and details fields.

### Decision 4: SQLModel relationship design (User → Tasks)

**Decision**: Implement one-to-many relationship with foreign key constraint and cascade deletion
**Rationale**: Enforces data integrity at database level, ensures tasks are automatically cleaned up when users are deleted, enables efficient querying with JOINs, prevents orphaned records in the database, supports the business requirement of user data isolation.
**Implementation**: User.id as primary key, Task.user_id as foreign key referencing User.id, Cascade delete on user removal, Index on user_id for efficient filtering.

### Decision 5: Frontend API client abstraction

**Decision**: Create centralized API client with built-in JWT token management
**Rationale**: Centralizes authentication logic in one place, simplifies API calls throughout the application, automatic token attachment to requests, consistent error handling across all API calls, easy to mock for testing purposes.
**Features**: Automatic JWT token inclusion in headers, token refresh on expiration, consistent error handling, request/response interceptors, type-safe API calls.

## Phase 1: Design & Contracts

### Architecture Diagram: Auth-Aware System

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

### API Contract Design

**Base URL**: `/api/v1`

**Endpoints**:
- `POST /users/register` - User registration
- `POST /users/login` - User authentication
- `GET /users/me` - Get authenticated user info
- `GET /users/{user_id}/tasks` - Get user's tasks (user_id from JWT)
- `POST /users/{user_id}/tasks` - Create user's task (user_id from JWT)
- `GET /users/{user_id}/tasks/{id}` - Get specific task (user_id from JWT)
- `PUT /users/{user_id}/tasks/{id}` - Update task (user_id from JWT)
- `DELETE /users/{user_id}/tasks/{id}` - Delete task (user_id from JWT)
- `PATCH /users/{user_id}/tasks/{id}/complete` - Mark task complete (user_id from JWT)

### Data Model Design

**User Model**:
- id: UUID (primary key)
- email: String (unique, indexed)
- hashed_password: String
- created_at: DateTime
- updated_at: DateTime

**Task Model**:
- id: UUID (primary key)
- title: String
- description: String (optional)
- completed: Boolean (default: False)
- user_id: UUID (foreign key to User)
- created_at: DateTime
- updated_at: DateTime

### Authentication Flow Design

1. User registers/logs in via Better Auth on frontend
2. Better Auth creates session and issues JWT token
3. Frontend stores token securely
4. Frontend makes API calls with Authorization: Bearer <token>
5. Backend extracts token from header, verifies signature using shared secret
6. Backend decodes token to get user_id and matches with request requirements
7. Backend filters data by authenticated user's ID

### Agent Responsibility Mapping

**Auth Agent**: User registration/login flows, JWT token generation/validation, password hashing/security, session management
**Frontend Agent**: UI components for authentication, secure token storage/management, API client implementation, user experience/feedback
**Backend Agent**: API endpoint implementation, JWT verification middleware/dependencies, business logic implementation, database interaction/validation
**DB Agent**: Schema design and relationships, data integrity constraints, user isolation enforcement, migration management

## Phase 2: Implementation Strategy

### Security Considerations
- All API requests require valid JWT token
- JWT verification on every request
- user_id derived from token, not request input
- Cross-user data access prevented at application and database level
- Unauthorized requests return 401
- Invalid/expired tokens rejected

### Error Handling Strategy
- 401 Unauthorized for missing/invalid tokens
- 403 Forbidden for insufficient permissions
- 404 Not Found for non-existent resources
- 422 Unprocessable Entity for validation errors
- Proper error messaging without exposing sensitive information

### Testing Strategy
- Signup/signin flow validation
- JWT issuance and expiry checks
- Missing/invalid token rejection
- Cross-user access prevention tests
- CRUD lifecycle tests per user
- Persistence verification in Neon DB