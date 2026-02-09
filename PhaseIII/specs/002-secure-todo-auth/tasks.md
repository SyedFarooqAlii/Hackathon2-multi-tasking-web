---
description: "Task breakdown for secure multi-user todo web app with refined auth architecture"
---

# Tasks: Secure Multi-User Todo Web App with JWT Authentication (Spec2)

**Input**: Design documents from `/specs/002-secure-todo-auth/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend/ and frontend/ directories
- [X] T002 [P] Initialize Python project with FastAPI dependencies in backend/
- [X] T003 [P] Initialize Next.js project with App Router in frontend/
- [X] T004 [P] Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup database schema and migrations framework using SQLModel in backend/src/core/database.py
- [X] T006 [P] Implement authentication/authorization framework with JWT in backend/src/core/security.py
- [X] T007 [P] Setup API routing and middleware structure in backend/src/main.py
- [X] T008 Create base models/entities that all stories depend on in backend/src/models/user.py
- [X] T009 Create base models/entities that all stories depend on in backend/src/models/task.py
- [X] T010 Configure error handling and logging infrastructure in backend/src/core/config.py
- [X] T011 Setup environment configuration management in backend/src/core/config.py
- [X] T012 Initialize Better Auth in frontend/src/lib/auth.ts
- [X] T013 Configure API client for JWT token handling in frontend/src/lib/api.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Todo Management (Priority: P1) 🎯 MVP

**Goal**: Users can securely manage their personal todo lists through a web application with proper authentication and data isolation.

**Independent Test**: Can be fully tested by creating a user account, logging in, creating todos, performing CRUD operations on those todos, and verifying that other users cannot access these todos.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Contract test for GET /api/v1/users/{user_id}/tasks in backend/tests/contract/test_todos.py
- [ ] T015 [P] [US1] Contract test for POST /api/v1/users/{user_id}/tasks in backend/tests/contract/test_todos.py
- [ ] T016 [P] [US1] Integration test for user todo management flow in backend/tests/integration/test_todo_management.py

### Implementation for User Story 1

- [ ] T017 [P] [US1] Create Todo model in backend/src/models/todo.py
- [X] T018 [US1] Implement TodoService in backend/src/services/todo_service.py
- [X] T019 [US1] Implement GET /api/v1/users/{user_id}/tasks endpoint in backend/src/api/v1/todos.py
- [X] T020 [US1] Implement POST /api/v1/users/{user_id}/tasks endpoint in backend/src/api/v1/todos.py
- [X] T021 [US1] Add validation and error handling for todo operations in backend/src/api/v1/todos.py
- [X] T022 [US1] Add logging for todo operations in backend/src/services/todo_service.py
- [ ] T023 [US1] Create Todo management component in frontend/src/components/todos/TodoList.tsx
- [ ] T024 [US1] Create Todo creation form in frontend/src/components/todos/TodoForm.tsx
- [ ] T025 [US1] Implement frontend API calls for todo operations in frontend/src/lib/api.ts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - JWT-Based Authentication (Priority: P1)

**Goal**: Users can register and authenticate using Better Auth with JWT tokens that are properly validated by the backend.

**Independent Test**: Can be tested by registering a new user, logging in to obtain a JWT token, and using that token to access protected endpoints.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T026 [P] [US2] Contract test for POST /api/v1/users/register in backend/tests/contract/test_auth.py
- [ ] T027 [P] [US2] Contract test for POST /api/v1/users/login in backend/tests/contract/test_auth.py
- [ ] T028 [P] [US2] Contract test for GET /api/v1/users/me in backend/tests/contract/test_auth.py
- [ ] T029 [P] [US2] Integration test for authentication flow in backend/tests/integration/test_auth.py

### Implementation for User Story 2

- [X] T030 [P] [US2] Create User model in backend/src/models/user.py
- [X] T031 [US2] Implement AuthService in backend/src/services/auth_service.py
- [X] T032 [US2] Implement POST /api/v1/users/register endpoint in backend/src/api/v1/auth.py
- [X] T033 [US2] Implement POST /api/v1/users/login endpoint in backend/src/api/v1/auth.py
- [X] T034 [US2] Implement GET /api/v1/users/me endpoint in backend/src/api/v1/auth.py
- [X] T035 [US2] Add JWT token generation and verification logic in backend/src/core/security.py
- [X] T036 [US2] Add authentication dependency for protected endpoints in backend/src/api/deps.py
- [ ] T037 [US2] Create authentication components in frontend/src/components/auth/Register.tsx
- [ ] T038 [US2] Create authentication components in frontend/src/components/auth/Login.tsx
- [ ] T039 [US2] Implement JWT token management in frontend/src/lib/auth.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Multi-User Data Isolation (Priority: P1)

**Goal**: Users can only access their own todo data, preventing unauthorized cross-user access.

**Independent Test**: Can be tested by having multiple users with their own tasks, then attempting to access or modify other users' tasks, and verifying that such access is denied.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T040 [P] [US3] Integration test for user data isolation in backend/tests/integration/test_data_isolation.py
- [ ] T041 [P] [US3] Contract test for user-specific resource access in backend/tests/contract/test_access_control.py

### Implementation for User Story 3

- [ ] T042 [P] [US3] Implement user_id derivation from JWT token in backend/src/api/deps.py
- [ ] T043 [US3] Add user_id validation in GET /api/v1/users/{user_id}/tasks to ensure it matches JWT in backend/src/api/v1/todos.py
- [ ] T044 [US3] Add user_id validation in POST /api/v1/users/{user_id}/tasks to ensure it matches JWT in backend/src/api/v1/todos.py
- [ ] T045 [US3] Add user_id validation in GET /api/v1/users/{user_id}/tasks/{id} to ensure it matches JWT in backend/src/api/v1/todos.py
- [ ] T046 [US3] Add user_id validation in PUT /api/v1/users/{user_id}/tasks/{id} to ensure it matches JWT in backend/src/api/v1/todos.py
- [ ] T047 [US3] Add user_id validation in DELETE /api/v1/users/{user_id}/tasks/{id} to ensure it matches JWT in backend/src/api/v1/todos.py
- [ ] T048 [US3] Add user_id validation in PATCH /api/v1/users/{user_id}/tasks/{id}/complete to ensure it matches JWT in backend/src/api/v1/todos.py
- [ ] T049 [US3] Update TaskService to enforce user ownership checks in backend/src/services/task_service.py
- [ ] T050 [US3] Add database-level filtering by user_id in TaskService queries in backend/src/services/task_service.py
- [ ] T051 [US3] Implement frontend logic to ensure user-specific data access in frontend/src/lib/api.ts

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: Remaining API Endpoints (Priority: P1)

**Goal**: Implement remaining task operation endpoints (GET by ID, UPDATE, DELETE, COMPLETE)

**Independent Test**: Can be tested by performing all 5 basic task operations (Add, View, Update, Delete, Complete) end-to-end.

### Tests for Remaining Endpoints (OPTIONAL - only if tests requested) ⚠️

- [ ] T052 [P] [US4] Contract test for GET /api/v1/users/{user_id}/tasks/{id} in backend/tests/contract/test_tasks.py
- [ ] T053 [P] [US4] Contract test for PUT /api/v1/users/{user_id}/tasks/{id} in backend/tests/contract/test_tasks.py
- [ ] T054 [P] [US4] Contract test for DELETE /api/v1/users/{user_id}/tasks/{id} in backend/tests/contract/test_tasks.py
- [ ] T055 [P] [US4] Contract test for PATCH /api/v1/users/{user_id}/tasks/{id}/complete in backend/tests/contract/test_tasks.py

### Implementation for Remaining Endpoints

- [ ] T056 [P] [US4] Implement GET /api/v1/users/{user_id}/tasks/{id} endpoint in backend/src/api/v1/tasks.py
- [ ] T057 [US4] Implement PUT /api/v1/users/{user_id}/tasks/{id} endpoint in backend/src/api/v1/tasks.py
- [ ] T058 [US4] Implement DELETE /api/v1/users/{user_id}/tasks/{id} endpoint in backend/src/api/v1/tasks.py
- [ ] T059 [US4] Implement PATCH /api/v1/users/{user_id}/tasks/{id}/complete endpoint in backend/src/api/v1/tasks.py
- [ ] T060 [US4] Add frontend components for viewing single task in frontend/src/components/tasks/TaskDetail.tsx
- [ ] T061 [US4] Add frontend components for updating task in frontend/src/components/tasks/TaskUpdate.tsx
- [ ] T062 [US4] Add frontend logic for toggling task completion status in frontend/src/components/tasks/TaskItem.tsx

**Checkpoint**: All basic task operations (Add, View, Update, Delete, Complete) are now implemented

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T063 [P] Documentation updates in docs/
- [ ] T064 Add comprehensive error handling and user feedback in frontend/src/components/ui/ErrorBoundary.tsx
- [ ] T065 Add loading states and user feedback in frontend/src/components/ui/LoadingSpinner.tsx
- [ ] T066 [P] Additional unit tests (if requested) in backend/tests/unit/
- [ ] T067 Add input validation and sanitization across all endpoints in backend/src/api/v1/
- [ ] T068 Security hardening and penetration testing checklist
- [ ] T069 Run quickstart.md validation to ensure all functionality works as expected

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P1)**: Depends on US1 and US2 being complete

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for GET /api/v1/users/{user_id}/tasks in backend/tests/contract/test_todos.py"
Task: "Contract test for POST /api/v1/users/{user_id}/tasks in backend/tests/contract/test_todos.py"
Task: "Integration test for user task management flow in backend/tests/integration/test_todo_management.py"

# Launch all models for User Story 1 together:
Task: "Create Todo model in backend/src/models/todo.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence