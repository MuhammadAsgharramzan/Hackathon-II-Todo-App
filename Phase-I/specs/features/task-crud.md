# Task CRUD Feature Specification

## Overview
This specification defines the Create, Read, Update, and Delete (CRUD) operations for tasks in the Todo Console App.

## Requirements

### Task Structure
Each task should contain:
- **ID**: Unique identifier (auto-generated)
- **Title**: Short description of the task (required)
- **Description**: Detailed description (optional)
- **Status**: Current state (e.g., "pending", "completed")
- **Created At**: Timestamp when task was created
- **Updated At**: Timestamp when task was last updated

### Create Operation
- **Command**: `add` or `create`
- **Input**: Title (required), Description (optional)
- **Output**: Success message with task ID
- **Validation**: Title must not be empty

### Read Operations
- **List All Tasks**: `list` command
  - Show all tasks with ID, Title, and Status
  - Sort by creation date (newest first)

- **View Single Task**: `view <id>` command
  - Show full task details including description
  - Handle invalid ID gracefully

### Update Operation
- **Command**: `update <id>`
- **Fields**: Title, Description, Status
- **Validation**: At least one field must be updated
- **Output**: Success message or error if task not found

### Delete Operation
- **Command**: `delete <id>`
- **Confirmation**: Prompt for confirmation before deletion
- **Output**: Success message or error if task not found

## Error Handling
- Invalid commands: Show help message
- Missing required fields: Clear error message
- Invalid task ID: "Task not found" message
- Empty task list: "No tasks found" message

## Data Persistence
- Tasks should be saved to a local file (JSON format)
- Data should persist between application sessions
- File location: `.todos.json` in user's home directory

## User Interface
- Command-line interface
- Clear prompts and feedback
- Color-coded status indicators (optional)

## Implementation Notes
- Use Python 3.13+ features
- Follow project constitution guidelines
- Include proper error handling
- Add input validation

# Feature: Task CRUD

## Task Model
- id: integer
- title: string
- description: string
- completed: boolean

## CLI Menu
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit

## Acceptance Criteria

### Add Task
- Ask for title
- Optional description
- Auto ID

### View Tasks
- Show ID, title, status

### Update Task
- Update title or description
- Error if ID not found

### Delete Task
- Delete by ID

### Toggle Complete
- Mark complete/incomplete
