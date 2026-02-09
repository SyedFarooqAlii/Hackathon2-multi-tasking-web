---
description: "Task list for Phase I Console Todo Application"
---

# Tasks: Phase I – In-Memory Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification does not explicitly request tests, but due to the quality requirements and success criteria, unit tests will be included to ensure proper functionality.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan with src/, tests/ directories
- [x] T002 Initialize Python project with proper directory structure (models/, services/, store/, cli/)
- [x] T003 [P] Configure basic project files (README.md, .gitignore, requirements.txt if needed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T004 Create base Task model in src/models/task.py following data model specification
- [x] T005 [P] Create in-memory store in src/store/in_memory_store.py with dictionary-based storage
- [x] T006 Create todo service in src/services/todo_service.py with basic CRUD operations
- [x] T007 Create CLI argument parser in src/cli/main.py to handle commands
- [x] T008 Configure error handling and validation infrastructure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement core functionality to add new tasks and view all tasks, enabling users to keep track of what they need to do.

**Independent Test**: Can be fully tested by adding tasks and viewing the list of all tasks. The system should maintain tasks in memory and display them consistently.

### Tests for User Story 1 (OPTIONAL - included for quality)
- [ ] T009 [P] [US1] Unit test for Task model in tests/unit/test_task.py
- [ ] T010 [P] [US1] Contract test for add command in tests/contract/test_cli_add.py
- [ ] T011 [P] [US1] Contract test for list command in tests/contract/test_cli_list.py

### Implementation for User Story 1
- [x] T012 [P] [US1] Implement Task model with validation rules in src/models/task.py
- [x] T013 [P] [US1] Implement in-memory store add_task method in src/store/in_memory_store.py
- [x] T014 [P] [US1] Implement in-memory store get_all_tasks method in src/store/in_memory_store.py
- [x] T015 [US1] Implement TodoService.add_task method in src/services/todo_service.py
- [x] T016 [US1] Implement TodoService.get_all_tasks method in src/services/todo_service.py
- [x] T017 [US1] Implement CLI add command handler in src/cli/main.py
- [x] T018 [US1] Implement CLI list command handler in src/cli/main.py
- [x] T019 [US1] Add validation for required fields (title not empty) in src/models/task.py
- [x] T020 [US1] Add sequential ID assignment in src/store/in_memory_store.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update and Complete Tasks (Priority: P2)

**Goal**: Implement functionality to update task details and mark tasks as complete, allowing users to track progress and modify task information.

**Independent Test**: Can be fully tested by updating task details and changing completion status. The system should persist these changes in memory for the duration of the session.

### Tests for User Story 2 (OPTIONAL - included for quality)
- [ ] T021 [P] [US2] Contract test for update command in tests/contract/test_cli_update.py
- [ ] T022 [P] [US2] Contract test for complete command in tests/contract/test_cli_complete.py

### Implementation for User Story 2
- [x] T023 [P] [US2] Implement in-memory store update_task method in src/store/in_memory_store.py
- [x] T024 [P] [US2] Implement in-memory store mark_complete/mark_incomplete methods in src/store/in_memory_store.py
- [x] T025 [US2] Implement TodoService.update_task method in src/services/todo_service.py
- [x] T026 [US2] Implement TodoService.mark_task_complete method in src/services/todo_service.py
- [x] T027 [US2] Implement TodoService.mark_task_incomplete method in src/services/todo_service.py
- [x] T028 [US2] Implement CLI update command handler in src/cli/main.py
- [x] T029 [US2] Implement CLI complete command handler in src/cli/main.py
- [x] T030 [US2] Implement CLI incomplete command handler in src/cli/main.py
- [x] T031 [US2] Add validation for task existence in update operations in src/services/todo_service.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Implement functionality to delete tasks that are no longer needed, allowing users to keep their todo list organized and relevant.

**Independent Test**: Can be fully tested by deleting tasks and verifying they no longer appear in the task list. The system should properly remove the task from memory.

### Tests for User Story 3 (OPTIONAL - included for quality)
- [ ] T032 [P] [US3] Contract test for delete command in tests/contract/test_cli_delete.py

### Implementation for User Story 3
- [x] T033 [P] [US3] Implement in-memory store delete_task method in src/store/in_memory_store.py
- [x] T034 [US3] Implement TodoService.delete_task method in src/services/todo_service.py
- [x] T035 [US3] Implement CLI delete command handler in src/cli/main.py
- [x] T036 [US3] Add validation for task existence in delete operations in src/services/todo_service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Error Handling & Edge Cases (Cross-cutting)

**Goal**: Implement proper error handling for all operations and handle edge cases identified in the specification

- [x] T037 [P] Add validation for non-existent task IDs across all operations in src/services/todo_service.py
- [x] T038 [P] Implement error message formatting for invalid operations per contract specifications
- [x] T039 Add validation for empty titles and field length limits per data model
- [x] T040 Add proper error handling for missing arguments in CLI argument parser
- [x] T041 [P] Add unit tests for error conditions in tests/unit/test_todo_service.py

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T042 [P] Documentation updates in README.md with usage instructions
- [x] T043 Code cleanup and refactoring across all modules
- [x] T044 [P] Integration tests for CLI in tests/integration/test_cli_integration.py
- [x] T045 [P] Additional unit tests (if needed) in tests/unit/
- [x] T046 Security hardening - input validation
- [x] T047 Run quickstart.md validation to ensure all commands work as specified

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Error Handling (Phase 6)**: Depends on all core functionality being implemented
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) SHOULD be written and FAIL before implementation
- Models before services
- Services before endpoints/cli
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