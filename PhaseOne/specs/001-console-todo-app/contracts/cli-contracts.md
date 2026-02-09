# CLI Command Contracts: Phase I – In-Memory Console Todo Application

**Date**: 2026-01-13
**Feature**: 001-console-todo-app

## Overview

This document defines the command-line interface contracts for the Todo application. Each command follows the pattern: `python todo.py <command> [arguments]`

## Command: Add Task
**Contract**: `python todo.py add <title> [description]`

### Input
- **title** (string, required): The title of the task to add
- **description** (string, optional): Additional details about the task

### Output
- **Success**: "Task added successfully with ID: <id>" where id is the assigned task ID
- **Error**: Appropriate error message if validation fails

### Requirements
- Assigns next available sequential ID
- Sets completion status to false by default
- Validates that title is not empty
- Returns unique ID for the created task

## Command: List Tasks
**Contract**: `python todo.py list`

### Input
- No arguments required

### Output
- **Success**: Formatted table showing all tasks with ID, Title, Description, and Status
- **Format**:
```
ID  | Title           | Description      | Status
----|-----------------|------------------|----------
1   | Buy groceries   | Milk, bread      | Incomplete
2   | Finish report   | Complete qtr rpt | Complete
```
- **Error**: Appropriate error message if system fails

### Requirements
- Shows all tasks in the system
- Displays correct completion status for each task
- Format output in a readable table structure

## Command: Update Task
**Contract**: `python todo.py update <id> <title> [description]`

### Input
- **id** (integer, required): The ID of the task to update
- **title** (string, required): The new title for the task
- **description** (string, optional): The new description for the task

### Output
- **Success**: "Task <id> updated successfully"
- **Error**: Appropriate error message if task ID doesn't exist or validation fails

### Requirements
- Validates that the task ID exists
- Updates only the specified fields (title and/or description)
- Preserves completion status
- Validates that title is not empty

## Command: Delete Task
**Contract**: `python todo.py delete <id>`

### Input
- **id** (integer, required): The ID of the task to delete

### Output
- **Success**: "Task <id> deleted successfully"
- **Error**: Appropriate error message if task ID doesn't exist

### Requirements
- Validates that the task ID exists before deletion
- Removes task from in-memory store
- Does not affect other tasks

## Command: Mark Complete/Incomplete
**Contract**: `python todo.py complete <id>` or `python todo.py incomplete <id>`

### Input
- **id** (integer, required): The ID of the task to update status

### Output
- **Success**: "Task <id> marked as <status>" where status is "complete" or "incomplete"
- **Error**: Appropriate error message if task ID doesn't exist

### Requirements
- Validates that the task ID exists
- Updates completion status to true (for complete) or false (for incomplete)
- Preserves other task fields

## Error Handling Contracts

### Invalid Command
- **Input**: Unknown command provided
- **Output**: "Error: Unknown command '<command>'. Use 'python todo.py help' for available commands."

### Missing Arguments
- **Input**: Command called without required arguments
- **Output**: "Error: Missing required arguments for '<command>'."

### Invalid ID
- **Input**: Command with non-existent task ID
- **Output**: "Error: Task with ID <id> does not exist."

### Validation Error
- **Input**: Command with invalid data (e.g., empty title)
- **Output**: "Error: <specific validation error message>"

## Success Criteria Validation
- All commands complete in under 1 second (per SC-002)
- All operations succeed with valid input (per SC-003)
- All error conditions return user-friendly messages (per SC-004)
- System maintains deterministic behavior (per SC-005)