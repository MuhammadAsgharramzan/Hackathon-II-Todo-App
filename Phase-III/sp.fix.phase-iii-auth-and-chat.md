# Phase-III Bug Fix Specification
## Fix Task Creation & Chatbot Errors

---

## Problem Summary
- Frontend task creation fails with "Failed to add task"
- Chatbot returns generic error when adding tasks
- No tasks are persisted in the database

---

## Root Cause
User identity (user_id) is not consistently derived from JWT and passed through:
- REST task endpoints
- Chat endpoint
- MCP tools

This causes authorization failures and database integrity errors.

---

## Fix Requirements

### 1. Authentication Consistency
- user_id MUST be extracted from JWT token in backend
- user_id MUST NOT be accepted from request body or frontend
- A shared dependency must be used to retrieve authenticated user

---

### 2. Backend Fixes (FastAPI)

#### a. JWT Dependency
- Create a dependency `get_current_user()`
- Decode JWT
- Return user object containing `id`

#### b. Task CRUD Endpoints
- Remove any `user_id` from request body
- Always use authenticated user.id
- Ensure queries are filtered by user.id

#### c. Chat Endpoint
- Extract user from JWT
- Pass user.id explicitly into agent context
- Never accept user_id from frontend request

---

### 3. MCP Tools Fix

For all MCP tools:
- Accept `user_id` as required parameter
- Validate ownership before DB operation
- Return structured error if user mismatch occurs

---

### 4. Agent Fixes

- Agent must inject `user_id` into every tool call
- Agent must never hallucinate user identity
- Agent must surface tool errors clearly

---

### 5. Frontend Fixes

- Ensure all API requests include:
  Authorization: Bearer <token>
- Do NOT send user_id in request payload
- Display backend error messages if request fails

---

## Validation Checklist

- [ ] User can add task via form
- [ ] User can add task via chatbot
- [ ] Tasks persist in database
- [ ] Tasks are user-isolated
- [ ] Chatbot confirms successful creation
- [ ] No generic "Sorry, error occurred" messages

---

## Implementation Instructions
Apply fixes incrementally:
1. Auth dependency
2. Task API
3. Chat endpoint
4. MCP tools
5. Agent wiring
6. Frontend API client

Do not skip steps.
