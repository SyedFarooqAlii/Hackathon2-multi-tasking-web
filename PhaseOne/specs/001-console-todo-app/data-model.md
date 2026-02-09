# Data Model: Phase I – In-Memory Console Todo Application

**Date**: 2026-01-13
**Feature**: 001-console-todo-app

## Entity: Task

### Fields
- **id** (integer): Unique identifier for the task, assigned sequentially starting from 1
- **title** (string): Descriptive name of the task, required field
- **description** (string): Detailed information about the task, optional field
- **completed** (boolean): Indicates whether the task is complete or incomplete, defaults to false

### Validation Rules
- **id**: Must be a positive integer, unique across all tasks in memory
- **title**: Must not be empty or null, maximum length 255 characters
- **description**: Optional, maximum length 1000 characters
- **completed**: Must be a boolean value (true/false)

### State Transitions
- **Initial State**: When created, `completed` is set to `false`
- **Complete Transition**: `completed` changes from `false` to `true` when marked complete
- **Incomplete Transition**: `completed` changes from `true` to `false` when marked incomplete

### Relationships
- No relationships with other entities (standalone entity for Phase I)

## In-Memory Store Structure

### Storage Mechanism
- **Type**: Dictionary (hash map) with integer keys
- **Key**: Task ID (integer)
- **Value**: Task object instance
- **Access Pattern**: O(1) lookup by ID

### Example Structure
```python
{
    1: Task(id=1, title="Buy groceries", description="Milk, bread, eggs", completed=False),
    2: Task(id=2, title="Finish report", description="Complete quarterly report", completed=True),
    3: Task(id=3, title="Call dentist", description="Schedule annual checkup", completed=False)
}
```

## Constraints
- All tasks exist only in memory (no persistence)
- Task IDs are stable and do not change once assigned
- Task IDs are sequential and start from 1
- Maximum recommended number of tasks: 1000 (for performance per SC-002)