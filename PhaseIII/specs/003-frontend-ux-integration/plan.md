# Implementation Plan: Frontend UX & API Client Integration

## Technical Context

This plan outlines the implementation of the frontend user experience and API client integration for the secure multi-user todo web application. The focus is on creating an intuitive user interface with seamless authentication and task management capabilities that properly integrate with the backend API using JWT tokens.

**Architecture Stack**:
- Frontend: Next.js 16+ with App Router
- Authentication: Better Auth integration
- State Management: React state/hooks with Better Auth session
- API Client: Custom client with JWT token management
- Styling: Tailwind CSS (or preferred framework)

**Integration Points**:
- Backend API endpoints for user authentication and todo operations
- Better Auth for user session management
- Database for user and todo persistence

**Unknowns**:
- Specific client-side fetch vs server actions approach (NEEDS CLARIFICATION)
- JWT injection mechanism (global fetch wrapper vs individual requests) (NEEDS CLARIFICATION)
- Route protection strategy (middleware vs layout guards) (NEEDS CLARIFICATION)
- Form handling and validation approach (NEEDS CLARIFICATION)

## Constitution Check

### Alignment with Project Principles
- **Security First**: All API requests must include JWT authentication
- **User Experience**: Loading states and error handling must be intuitive
- **Modularity**: Components should be reusable and maintainable
- **Performance**: Efficient data fetching and state management

### Compliance Verification
- [ ] Authentication state properly isolated between users
- [ ] JWT tokens stored securely in browser
- [ ] Error states handled gracefully
- [ ] Loading states provide user feedback
- [ ] Form validation prevents invalid submissions

### Gate Evaluation
- [ ] All security requirements met before deployment
- [ ] User privacy maintained throughout experience
- [ ] Error handling protects system integrity
- [ ] Performance targets achieved

## Phase 0: Research & Decision Making

### Research Task 1: Client-Side Fetch vs Server Actions
**Objective**: Determine the optimal approach for API calls in Next.js App Router

**Decision**: Client-side fetch with SWR/react-query for dynamic updates
**Rationale**: Provides real-time updates for todo operations while maintaining SEO benefits
**Alternatives considered**: Server actions, pure server components, client components only

### Research Task 2: JWT Injection Mechanism
**Objective**: Determine where and how JWT tokens are injected into requests

**Decision**: Axios interceptors with global configuration
**Rationale**: Automatically attaches tokens to all requests, handles token refresh
**Alternatives considered**: Manual attachment per request, React context provider

### Research Task 3: Route Protection Strategy
**Objective**: Determine the best approach for protecting routes in Next.js App Router

**Decision**: Middleware-based protection with session validation
**Rationale**: Provides server-side protection, prevents unauthorized access early
**Alternatives considered**: Client-side guards in layouts, HOC wrappers

### Research Task 4: Form Handling and Validation Approach
**Objective**: Determine the optimal form handling and validation strategy

**Decision**: React Hook Form with Zod for validation
**Rationale**: Provides excellent developer experience with strong typing
**Alternatives considered**: Native form handling, Formik, controlled components only

## Phase 1: Architecture Design

### 1.1 Frontend Architecture with Next.js App Router

#### Directory Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── (protected)/
│   │   ├── dashboard/
│   │   ├── todos/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/
│   │   │   └── create/
│   │   └── layout.tsx
│   ├── layout.tsx
│   ├── page.tsx
│   └── middleware.ts
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── todos/
│   │   ├── TodoList.tsx
│   │   ├── TodoItem.tsx
│   │   ├── TodoForm.tsx
│   │   └── TodoFilters.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Card.tsx
├── lib/
│   ├── api.ts
│   ├── auth.ts
│   ├── types.ts
│   └── utils.ts
├── hooks/
│   ├── useTodos.ts
│   └── useAuth.ts
└── providers/
    └── AuthProvider.tsx
```

#### Component Architecture
- **Layout Components**: Shared layouts with authentication awareness
- **Page Components**: Feature-specific views with minimal logic
- **UI Components**: Reusable presentation components
- **Hook Components**: Business logic encapsulation
- **Provider Components**: Global state management

### 1.2 Auth-Aware Page Structure

#### Public Routes (Accessible without authentication)
- `/` - Landing page
- `/login` - User login
- `/register` - User registration

#### Protected Routes (Require authentication)
- `/dashboard` - User dashboard
- `/todos` - Todo management
- `/todos/create` - Create new todo
- `/todos/[id]` - Todo detail view

#### Route Protection Implementation
```typescript
// middleware.ts
import { authMiddleware } from 'next-auth/middleware'
import { withAuth } from 'next-auth/middleware'

export default withAuth({
  pages: {
    signIn: '/login',
  },
})

export const config = {
  matcher: ['/dashboard/:path*', '/todos/:path*']
}
```

### 1.3 Centralized API Client for Backend Communication

#### API Client Architecture
```typescript
// lib/api.ts
class ApiClient {
  private baseUrl: string
  private token: string | null

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'
    this.token = null
  }

  // Configure axios with interceptors for JWT handling
  private setupAxiosInterceptors() {
    axios.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized - clear token and redirect
          this.clearToken()
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Authentication methods
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    // Implementation
  }

  async register(userData: RegisterData): Promise<AuthResponse> {
    // Implementation
  }

  // Todo methods
  async getTodos(): Promise<Todo[]> {
    // Implementation
  }

  async createTodo(todoData: TodoCreate): Promise<Todo> {
    // Implementation
  }

  async updateTodo(id: string, todoData: TodoUpdate): Promise<Todo> {
    // Implementation
  }

  async deleteTodo(id: string): Promise<void> {
    // Implementation
  }

  async toggleTodoCompletion(id: string, completed: boolean): Promise<Todo> {
    // Implementation
  }
}
```

### 1.4 UX Flow for Todo Lifecycle

#### Add Todo Flow
1. User clicks "Add Todo" button
2. Modal/form appears with title and description fields
3. User fills in details and submits
4. Loading state shows during API call
5. Success: Todo appears in list with success feedback
6. Error: Error message displayed

#### List Todos Flow
1. User accesses todos page
2. Loading skeleton shows during data fetch
3. Todos display in organized list
4. Pagination/filtering available for many todos

#### Update Todo Flow
1. User clicks edit icon on todo item
2. Inline editor or modal appears
3. User modifies title/description
4. Changes saved automatically or via save button
5. Success/error feedback provided

#### Delete Todo Flow
1. User clicks delete icon on todo item
2. Confirmation dialog appears
3. User confirms deletion
4. Todo removed with animation
5. Undo option available briefly

#### Complete Todo Flow
1. User toggles checkbox on todo item
2. Visual feedback shows status change
3. API call updates completion status
4. Success/error feedback provided

### 1.5 Error and Loading State Handling Strategy

#### Loading States
- **Global Loading**: Full page loader for initial data fetch
- **Component Loading**: Skeleton loaders for specific sections
- **Button Loading**: Visual feedback during form submissions
- **Progressive Loading**: Optimistic updates where appropriate

#### Error States
- **Network Errors**: Clear messaging with retry option
- **Validation Errors**: Field-specific error messages
- **Authentication Errors**: Redirect to login with preserved context
- **Permission Errors**: Clear messaging about access restrictions

#### Error Boundaries
```typescript
// components/ErrorBoundary.tsx
class ErrorBoundary extends React.Component {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to monitoring service
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong.</div>
    }
    return this.props.children
  }
}
```

## Phase 2: Data Model and API Contracts

### 2.1 Data Model (data-model.md)

#### User Entity
- **Fields**:
  - id: string (UUID)
  - email: string (unique, required)
  - created_at: DateTime
  - updated_at: DateTime
- **Validations**: Email format validation, uniqueness constraint
- **Relationships**: One-to-many with Todo entities

#### Todo Entity
- **Fields**:
  - id: string (UUID)
  - title: string (required, max 255 chars)
  - description: string (optional)
  - completed: boolean (default false)
  - user_id: string (foreign key to User)
  - created_at: DateTime
  - updated_at: DateTime
- **Validations**: Title required, length constraints
- **Relationships**: Many-to-one with User entity

### 2.2 API Contracts

#### Authentication Endpoints
```
POST /api/v1/users/register
- Request: { email: string, password: string }
- Response: { access_token: string, token_type: string }

POST /api/v1/users/login
- Request: { email: string, password: string }
- Response: { access_token: string, token_type: string }

GET /api/v1/users/me
- Headers: Authorization: Bearer {token}
- Response: { id: string, email: string, created_at: string, updated_at: string }
```

#### Todo Endpoints
```
GET /api/v1/users/me/tasks
- Headers: Authorization: Bearer {token}
- Response: { tasks: [{ id, title, description, completed, user_id, created_at, updated_at }] }

POST /api/v1/users/me/tasks
- Headers: Authorization: Bearer {token}
- Request: { title: string, description?: string, completed?: boolean }
- Response: { id, title, description, completed, user_id, created_at, updated_at }

GET /api/v1/users/me/tasks/{id}
- Headers: Authorization: Bearer {token}
- Response: { id, title, description, completed, user_id, created_at, updated_at }

PUT /api/v1/users/me/tasks/{id}
- Headers: Authorization: Bearer {token}
- Request: { title?: string, description?: string, completed?: boolean }
- Response: { id, title, description, completed, user_id, created_at, updated_at }

DELETE /api/v1/users/me/tasks/{id}
- Headers: Authorization: Bearer {token}
- Response: { message: string }

PATCH /api/v1/users/me/tasks/{id}/complete
- Headers: Authorization: Bearer {token}
- Request: { completed: boolean }
- Response: { id, title, description, completed, user_id, created_at, updated_at }
```

## Phase 3: Quickstart Guide

### 3.1 Prerequisites
- Node.js 18+ installed
- Yarn or npm package manager
- Access to backend API server

### 3.2 Setup Instructions
```bash
# Clone the repository
git clone <repository-url>
cd frontend

# Install dependencies
yarn install

# Copy environment variables
cp .env.example .env.local

# Update environment variables
NEXT_PUBLIC_API_BASE_URL=<backend-api-url>
NEXTAUTH_SECRET=<secret-for-auth>
NEXTAUTH_URL=<frontend-url>

# Start development server
yarn dev
```

### 3.3 Development Workflow
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes following component architecture
3. Run tests: `yarn test`
4. Format code: `yarn format`
5. Lint code: `yarn lint`
6. Commit changes with conventional commits
7. Push and create pull request

### 3.4 Testing Strategy
- Unit tests for individual components
- Integration tests for API client
- End-to-end tests for critical user flows
- Accessibility testing with automated tools

## Phase 4: Implementation Roadmap

### Sprint 1: Authentication Infrastructure
- [ ] Set up Next.js App Router structure
- [ ] Integrate Better Auth for user management
- [ ] Implement login and registration forms
- [ ] Create protected route middleware
- [ ] Set up global state management

### Sprint 2: API Client and Data Layer
- [ ] Implement centralized API client
- [ ] Create type definitions for all entities
- [ ] Set up data fetching hooks
- [ ] Implement error handling strategy
- [ ] Add loading state management

### Sprint 3: Todo Management Interface
- [ ] Create todo listing component
- [ ] Implement todo creation form
- [ ] Add todo editing functionality
- [ ] Create todo completion toggle
- [ ] Implement todo deletion with confirmation

### Sprint 4: UX Polish and Testing
- [ ] Add loading skeletons and animations
- [ ] Implement comprehensive error handling
- [ ] Add form validation and user feedback
- [ ] Conduct accessibility testing
- [ ] Performance optimization

## Phase 5: Risk Assessment

### High-Risk Areas
- **Authentication Security**: Ensure JWT tokens are stored securely
- **Cross-Site Request Forgery**: Implement proper CSRF protection
- **Data Privacy**: Verify user data isolation between accounts

### Mitigation Strategies
- Regular security audits of authentication implementation
- Input validation on both frontend and backend
- Comprehensive error handling to prevent information disclosure
- Automated testing for authentication flows

## Phase 6: Success Metrics

### Technical Metrics
- API response time under 500ms for 95% of requests
- Page load time under 3 seconds on 3G connection
- Zero critical security vulnerabilities
- 90% code coverage for authentication flows

### User Experience Metrics
- Registration completion rate >80%
- Successful login rate >95%
- Todo operation success rate >98%
- User session persistence rate >99%

This implementation plan provides a comprehensive roadmap for developing the frontend UX and API client integration while maintaining security, performance, and usability standards.