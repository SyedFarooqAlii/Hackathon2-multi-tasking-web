# Research: Authenticated Full-Stack Todo Web Application

**Feature**: 001-auth-fullstack-todo | **Date**: 2026-01-16

## Research Summary

This document captures the research findings for implementing the authenticated full-stack todo web application with JWT-based authentication, focusing on technology decisions and best practices.

## Decision: JWT-based Authentication vs Session-based Authentication

**Decision**: Choose JWT-based authentication
**Rationale**:
- Stateless design enables horizontal scaling without shared session storage
- Self-contained tokens carry user information and permissions
- Better security through token expiration and verification
- Enables microservices architecture without session coupling
- Better for mobile and API-heavy applications

**Alternatives considered**:
- Session-based: Requires server-side session storage, harder to scale horizontally
- OAuth 2.0: More complex for basic user authentication needs

## Decision: Better Auth + FastAPI JWT Verification Strategy

**Decision**: Use Better Auth for frontend authentication with FastAPI backend verification
**Rationale**:
- Better Auth handles user registration/login securely with established patterns
- FastAPI provides excellent support for JWT verification with middleware
- Maintains separation of concerns between frontend authentication and backend authorization
- Stateless design eliminates session coupling between frontend and backend

**Implementation approach**:
- Frontend: Better Auth handles registration/login and token management
- Backend: FastAPI middleware extracts and verifies JWT tokens
- Shared secret for JWT signing/verification between services

## Decision: User ID Derivation from JWT Token

**Decision**: Always derive user_id from JWT token, never trust from request path
**Rationale**:
- Critical security measure to prevent user ID spoofing
- Request parameters can be manipulated by malicious clients
- JWT tokens are cryptographically signed and verified
- Ensures users can only access their own data regardless of request parameters

## Decision: SQLModel Schema with User Ownership

**Decision**: Include user_id foreign key in Todo model for database-level enforcement
**Rationale**:
- Provides additional security layer alongside application-level checks
- Enables efficient database queries with JOINs and WHERE clauses
- Supports data isolation at the persistence layer
- Prevents accidental data leakage due to application bugs

## Technology Stack Research

### Next.js 16+ (App Router)
- Modern React framework with file-based routing
- Server Components and Streaming capabilities
- Built-in optimization features
- Excellent TypeScript support
- Strong ecosystem and community

### FastAPI
- Modern Python web framework with async support
- Automatic API documentation (Swagger/OpenAPI)
- Strong typing with Pydantic
- High performance comparable to Node.js frameworks
- Excellent for building APIs with automatic validation

### SQLModel
- Combines SQLAlchemy and Pydantic
- Type-safe database models
- Seamless integration with FastAPI
- Supports async operations
- Good for complex data relationships

### Neon PostgreSQL
- Serverless PostgreSQL with instant branching
- Pay-per-use pricing model
- PostgreSQL compatibility
- Built-in connection pooling
- Easy scaling and management

### Better Auth
- Modern authentication library for React/Next.js
- Supports JWT tokens
- Handles user registration/login securely
- Integrates well with various databases
- Provides session management

## Security Best Practices Researched

### JWT Security
- Use strong secret keys for signing
- Implement proper token expiration
- Store tokens securely on client (preferably in httpOnly cookies)
- Validate token signatures on every request
- Use HTTPS in production

### API Security
- Rate limiting to prevent abuse
- Input validation and sanitization
- Proper error handling without information disclosure
- Authentication and authorization on all endpoints
- Use HTTPS for all communications

## Architecture Patterns Researched

### Layered Architecture
- Presentation layer (Next.js frontend)
- Service layer (FastAPI backend)
- Data access layer (SQLModel/PostgreSQL)
- Clear separation of responsibilities
- Easier testing and maintenance

### Statelessness
- No server-side session storage
- JWT tokens contain necessary user information
- Scalable architecture without shared state
- Each request contains all necessary information

## Testing Strategy Researched

### Unit Testing
- Individual function/method testing
- Mock external dependencies
- Fast execution and comprehensive coverage

### Integration Testing
- API endpoint testing
- Database interaction testing
- Authentication flow testing
- Cross-component interaction testing

### End-to-End Testing
- Complete user flow testing
- Frontend-backend integration testing
- Authentication and authorization testing
- Real-world scenario testing