# Phase-III Specification
## Todo AI Chatbot with MCP & Agents SDK

---

## Objective
Transform the existing Todo web application into an AI-powered chatbot that allows users to manage their tasks using natural language commands.

---

## In-Scope Features

### 1. Conversational Task Management
The chatbot must support:
- Creating tasks
- Listing tasks
- Updating tasks
- Completing tasks
- Deleting tasks

All operations must be triggered via natural language.

---

### 2. Chat API
**Endpoint**
POST /api/chat

**Request**
- conversation_id (optional)
- message (required string)

**Response**
- conversation_id
- assistant_response
- tool_calls (if any)

---

### 3. Conversation Persistence
The system must store:
- Conversations
- Messages (user + assistant)
- Tool invocation metadata

Conversation history must be retrieved on every request.

---

## MCP Tools Specification

### Tool: add_task
**Purpose:** Create a new todo task

Parameters:
- user_id (string, required)
- title (string, required)
- description (string, optional)

Returns:
- task_id
- status
- title

---

### Tool: list_tasks
**Purpose:** Retrieve tasks for a user

Parameters:
- user_id (string, required)
- status (optional: all | pending | completed)

Returns:
- list of tasks

---

### Tool: update_task
**Purpose:** Modify a task

Parameters:
- user_id (string, required)
- task_id (integer, required)
- title (optional)
- description (optional)

Returns:
- task_id
- status
- title

---

### Tool: complete_task
**Purpose:** Mark task as completed

Parameters:
- user_id (string, required)
- task_id (integer, required)

Returns:
- task_id
- status
- title

---

### Tool: delete_task
**Purpose:** Remove a task

Parameters:
- user_id (string, required)
- task_id (integer, required)

Returns:
- task_id
- status
- title

---

## Agent Behavior Rules

### Intent Mapping
| User Intent | Tool Action |
|------------|------------|
| "Add", "Remember", "Create" | add_task |
| "Show", "List", "What are" | list_tasks |
| "Done", "Complete" | complete_task |
| "Delete", "Remove" | delete_task |
| "Change", "Update" | update_task |

---

### Confirmation Rules
- Every successful action must be confirmed in natural language.
- Example: “✅ Task ‘Buy groceries’ has been added.”

---

### Error Handling
- If a task is not found, respond politely.
- If input is ambiguous, ask a clarifying question.
- Never expose stack traces or internal errors.

---

## Database Models

### Conversation
- id
- user_id
- created_at
- updated_at

### Message
- id
- conversation_id
- user_id
- role (user | assistant)
- content
- created_at

---

## Frontend (Chat UI)
- Use OpenAI ChatKit
- Stateless UI
- Displays conversation history
- Shows confirmations and errors clearly

---

## Acceptance Criteria
- User can manage todos without touching UI buttons.
- Agent always uses MCP tools.
- Backend remains stateless.
- Restarting server does not lose chat history.

---

## Out of Scope
- Voice input
- Multi-language support
- Advanced planning or scheduling