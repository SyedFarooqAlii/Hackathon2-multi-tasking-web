# Quickstart Guide: Phase I – In-Memory Console Todo Application

**Date**: 2026-01-13
**Feature**: 001-console-todo-app

## Prerequisites

- Python 3.13 or higher installed on your system
- Command-line interface (Terminal on macOS/Linux, Command Prompt or PowerShell on Windows)

## Setup

1. Clone or access the project directory containing the Todo application source code
2. Ensure you have Python 3.13+ installed by running:
   ```bash
   python --version
   ```
3. Navigate to the project root directory where the application is located

## Running the Application

The application runs directly as a Python script without any installation or compilation needed:

```bash
python src/cli/main.py [command] [arguments]
```

## Available Commands

### Add a New Task
```bash
python src/cli/main.py add "Task Title" "Optional description"
```

**Example:**
```bash
python src/cli/main.py add "Buy groceries" "Milk, bread, eggs, fruits"
```

### List All Tasks
```bash
python src/cli/main.py list
```

**Example:**
```bash
python src/cli/main.py list
```

### Update an Existing Task
```bash
python src/cli/main.py update <task_id> "New Title" "Optional new description"
```

**Example:**
```bash
python src/cli/main.py update 1 "Buy weekly groceries" "Milk, bread, eggs, fruits, vegetables"
```

### Delete a Task
```bash
python src/cli/main.py delete <task_id>
```

**Example:**
```bash
python src/cli/main.py delete 1
```

### Mark a Task as Complete
```bash
python src/cli/main.py complete <task_id>
```

**Example:**
```bash
python src/cli/main.py complete 1
```

### Mark a Task as Incomplete
```bash
python src/cli/main.py incomplete <task_id>
```

**Example:**
```bash
python src/cli/main.py incomplete 1
```

## Sample Workflow

1. Add a task:
   ```bash
   python src/cli/main.py add "Finish project proposal" "Complete the Q1 project proposal document"
   # Output: Task added successfully with ID: 1
   ```

2. Add another task:
   ```bash
   python src/cli/main.py add "Schedule team meeting" "Set up meeting for project discussion"
   # Output: Task added successfully with ID: 2
   ```

3. List all tasks:
   ```bash
   python src/cli/main.py list
   # Output:
   # ID  | Title                  | Description                        | Status
   # ----|------------------------|------------------------------------|----------
   # 1   | Finish project proposal| Complete the Q1 project proposal  | Incomplete
   # 2   | Schedule team meeting  | Set up meeting for project discuss| Incomplete
   ```

4. Mark a task as complete:
   ```bash
   python src/cli/main.py complete 1
   # Output: Task 1 marked as complete
   ```

5. List tasks again to see the updated status:
   ```bash
   python src/cli/main.py list
   # Shows updated status for task 1
   ```

## Error Handling

- If you provide an invalid task ID, you'll see: "Error: Task with ID <id> does not exist."
- If you provide insufficient arguments to a command, you'll see: "Error: Missing required arguments for '<command>'."
- If you use an unknown command, you'll see: "Error: Unknown command '<command>'."

## Notes

- All data is stored in-memory only and will be lost when the application exits
- Task IDs are assigned sequentially starting from 1
- The application behaves deterministically - the same inputs will always produce the same outputs
- For best performance, it's recommended to keep the number of tasks under 1000