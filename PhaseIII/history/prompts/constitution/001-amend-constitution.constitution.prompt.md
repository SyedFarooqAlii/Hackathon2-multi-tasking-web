---
id: "001"
title: "Amend Constitution"
stage: "constitution"
date_iso: "2026-01-16"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-console-todo-app"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "governance", "standards"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
 - none
---

# PHR: Amend Constitution

## Outcome

Updated the project constitution to reflect the specific requirements for the Phase II Todo Full-Stack Web Application with Multi-User Authentication.

## Evaluation

The constitution was successfully updated from the template with concrete values reflecting the project requirements:
- Spec-driven development principles
- Security-first authentication and authorization
- Clear separation of concerns
- Deterministic agent workflow
- User data isolation enforcement
- Architecture standards (Next.js, FastAPI, SQLModel, Neon PostgreSQL, Better Auth)
- Security rules for JWT-based authentication
- API standards for RESTful endpoints
- Development workflow constraints following Agentic Dev Stack

## Prompt Text

```
/sp.constitution

Project: Phase II – Todo Full-Stack Web Application (Multi-User, Authenticated)

Core principles:
- Spec-driven development (all implementation must follow written specs)
- Security-first authentication and authorization
- Clear separation of concerns (Frontend, Backend, Database, Auth)
- Deterministic, reviewable agent workflow (no manual coding)
- User data isolation and ownership enforcement

Key standards:
- All features must be derived directly from approved specs
- Every API endpoint must enforce JWT-based authentication
- Task ownership must be validated on every read/write operation
- Frontend, backend, and auth flows must remain consistent
- Errors must be explicit, user-safe, and spec-defined
- Code must follow clean architecture and modern best practices

Architecture standards:
- Frontend: Next.js 16+ App Router
- Backend: FastAPI (Python)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Shared JWT secret via environment variables
- Stateless backend authentication (no session coupling)

Security rules:
- All API requests require a valid JWT token
- JWT must be verified on every request
- user_id must be derived from token, not trusted from client input
- Cross-user data access is strictly forbidden
- Unauthorized requests must return 401
- Invalid or expired tokens must be rejected

API standards:
- RESTful endpoints only
- Endpoints remain stable but behavior is auth-enforced
- All queries filtered by authenticated user
- Task ownership enforced on create, read, update, delete, complete

Development workflow constraints:
- Follow Agentic Dev Stack strictly:
  Spec → Plan → Tasks → Implementation
- Use Claude Code + Spec-Kit Plus only
- No manual coding outside Claude Code
- All decisions must be documented in specs
- Iterations must preserve backward correctness

Deliverable standards:
- Fully functional authenticated web app
- Persistent storage via Neon PostgreSQL
- Responsive frontend UI
- Secure multi-user task manag
```

## Response Text

Successfully updated the constitution file with all project-specific principles and standards. Created 6 core principles covering spec-driven development, security, separation of concerns, agent workflow, data isolation, and clean architecture. Added sections for Additional Constraints, Architecture Standards, Security Rules, API Standards, Development Workflow Constraints, and Deliverable Standards. The constitution now properly reflects the requirements for the Phase II Todo Full-Stack Web Application.