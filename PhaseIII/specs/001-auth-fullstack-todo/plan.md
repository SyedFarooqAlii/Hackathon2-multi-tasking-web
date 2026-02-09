# Implementation Plan: Authenticated Full-Stack Todo Web Application

**Branch**: `001-auth-fullstack-todo` | **Date**: 2026-01-16 | **Spec**: ../spec.md
**Input**: Feature specification from `/specs/001-auth-fullstack-todo/spec.md`

## Summary

Design and implement a secure, multi-user todo web application with JWT-based authentication using Better Auth, Next.js frontend, FastAPI backend, and Neon PostgreSQL database. The system will enforce strict user data isolation and follow a stateless authentication architecture.

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
specs/001-auth-fullstack-todo/
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
│   │   └── todo.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── todo_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── todos.py
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
│   │   └── todos/
│   ├── components/
│   │   ├── auth/
│   │   ├── todos/
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

### Decision 1: JWT-based auth vs session-based auth

**Decision**: Choose JWT-based authentication
**Rationale**: Stateless design enables horizontal scaling, reduces server-side session storage overhead, and provides better security through token expiration and verification. Better Auth supports JWT tokens that can be verified by any service with the shared secret.
**Alternatives considered**: Traditional session-based authentication, OAuth 2.0

### Decision 2: Better Auth on frontend + FastAPI verification strategy

**Decision**: Use Better Auth for frontend authentication and JWT token issuance, with FastAPI backend responsible for token verification
**Rationale**: Better Auth handles user registration/login securely, while FastAPI can verify JWT tokens independently without session coupling, maintaining statelessness.
**Alternatives considered**: Custom auth implementation, third-party providers only

### Decision 3: user_id derivation from JWT vs request path

**Decision**: Derive user_id from JWT token, not from request path parameters
**Rationale**: Security requirement to prevent user ID spoofing. Request path parameters can be manipulated by clients, but JWT tokens contain verified user identity.
**Alternatives considered**: Trusting user_id from request path (insecure)

### Decision 4: SQLModel schema design for multi-user task ownership

**Decision**: Include user_id foreign key in Todo model to enforce ownership at database level
**Rationale**: Database-level enforcement provides additional security layer alongside application-level checks.
**Alternatives considered**: No ownership field (wouldn't meet requirements)

## Phase 1: Design & Contracts

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
- created_at: DateTime
- updated_at: DateTime

**Todo Model**:
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
- Auth flow validation (signup, signin, token issuance)
- JWT verification and rejection cases
- User isolation tests (cross-user access blocked)
- CRUD operation tests per authenticated user
- Frontend → Backend integration tests
- Persistence verification using Neon PostgreSQL