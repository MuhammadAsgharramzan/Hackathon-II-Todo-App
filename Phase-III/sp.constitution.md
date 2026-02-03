# Phase-III Constitution
## Todo AI Chatbot – Architecture of Intelligence

### Purpose
This constitution defines the non-negotiable rules, principles, and constraints for Phase-III of the Evolution of Todo project.  
The goal of Phase-III is to evolve the Todo application into an AI-powered, stateless, cloud-ready chatbot using Agentic Architecture and MCP (Model Context Protocol).

---

## Core Principles

### 1. Spec-Driven Development (Mandatory)
- All functionality MUST originate from specifications.
- No code may be written manually by a human.
- Claude Code is the sole implementation agent.
- If output is incorrect, the specification must be refined — not the code.

---

### 2. Stateless Backend Architecture
- The FastAPI server MUST remain stateless.
- No in-memory session storage is allowed.
- All conversation state MUST be persisted in the database.
- Every request must be independently processable.

---

### 3. Tool-First Agent Design
- The AI agent MUST NOT manipulate the database directly.
- All task operations MUST occur via MCP tools.
- The agent reasons → selects tools → executes tools → responds.
- Tools are the only allowed bridge between AI and application logic.

---

### 4. Deterministic & Auditable Behavior
- All tool calls must be logged.
- All user and assistant messages must be stored.
- Agent decisions should be explainable from logs and history.
- No hidden side effects.

---

### 5. Security & User Isolation
- Every request must be authenticated using JWT.
- User identity must be derived from the verified token.
- MCP tools MUST enforce user ownership.
- A user can only read/write their own tasks and conversations.

---

### 6. Graceful Error Handling
- Errors must never crash the agent.
- Tool failures should result in friendly user-facing messages.
- “Task not found”, “Invalid input”, and “Unauthorized” must be handled explicitly.

---

### 7. Incremental Intelligence
- Start with Basic Level features only.
- No advanced AI features without explicit specs.
- Intelligence should increase via specs, not heuristics.

---

## Non-Goals (Explicitly Forbidden)
- No hardcoded logic in agent responses.
- No direct SQL usage inside agent code.
- No coupling between frontend UI and agent logic.
- No business logic outside MCP tools.

---

## Success Criteria
Phase-III is considered complete when:
- Users can manage todos using natural language.
- AI agent correctly uses MCP tools.
- Conversation state survives server restarts.
- The system is ready for Kubernetes deployment in Phase-IV.
