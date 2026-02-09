# Phase I – In-Memory Console Todo Application

An interactive menu-driven todo application that runs entirely in memory.

## Features
- Add new tasks with title and description
- List all tasks with their status
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- Interactive menu-driven interface
- Tasks remain in memory during the session

## Usage

### Interactive Mode (Recommended)
```bash
python src/cli/main.py
```

This starts an interactive session with a menu:
```
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit
```

### Command Line Mode (Original)
```bash
python src/cli/main.py add "Task Title" "Optional description"
python src/cli/main.py list
python src/cli/main.py update 1 "New Title" "Optional new description"
python src/cli/main.py delete 1
python src/cli/main.py complete 1
python src/cli/main.py incomplete 1
```

## Key Improvements

The application now features an **interactive menu-driven interface** that maintains tasks in memory during the session, allowing multiple operations without losing data between commands.