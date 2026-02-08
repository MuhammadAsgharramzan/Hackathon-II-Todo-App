---
name: "container-service"
description: "Containerize applications using Docker, handling dependencies, Dockerfiles, and build optimizations."
version: "1.0.0"
---

# Container Service Skill

## When to Use This Skill
- User wants to "dockerize" an application (frontend or backend).
- User needs to create or fix `Dockerfile`.
- User encounters build errors related to dependencies or context size.
- User wants to optimize Docker images (multi-stage builds, .dockerignore).

## How This Skill Works

1.  **Analyze Project Structure**: Identify language (Python/Node), entry points (`main.py`, `package.json`), and existing configuration.
2.  **Check Prerequisites**: Ensure Docker Engine is running and accessible (`docker version`).
3.  **Draft/Verify Dockerfile**:
    *   **Backend (Python)**: Use slim images, multistage builds if needed, install system deps (gcc, libpq-dev), install python deps (requirements.txt).
    *   **Frontend (Node/Next.js)**: Use multistage builds (deps -> builder -> runner), use `standalone` output for Next.js.
4.  **Optimize Build Context**: Create `.dockerignore` to exclude `node_modules`, `venv`, `.git`, temporary files. This is CRITICAL for build speed.
5.  **Dependency Resolution**: Check `requirements.txt` or `package.json` for conflicts (e.g., version pinning issues). Upgrade/Unpin packages if build fails.
6.  **Build & Verify**: Run `docker build -t <name> .`. check for success.

## Output Format

Provide:
- **Status Checks**: "Docker Engine is [Active/Inactive]"
- **File Actions**: "[Created/Updated] Dockerfile", "[Created] .dockerignore"
- **Build Logs**: Summary of build process (success/failure).
- **Fix Actions**: "Unpinned [package] to resolve conflict."

## Quality Criteria
- Dockerfile use specific (but flexible) base images (e.g., `python:3.12-slim`).
- `.dockerignore` exists and includes heavy folders.
- Build completes with `Exit code: 0`.
- Application runs inside container (optional verification step).

## Example

**Input**: "Containerize this FastAPI backend."

**Output**:
1.  **Analysis**: Found `main.py` and `requirements.txt`.
2.  **Dockerfile**: Created multistage Dockerfile.
3.  **Optimization**: Created `.dockerignore` excluding `venv`.
4.  **Build**: Executed `docker build -t todo-backend:latest .`.
5.  **Result**: Build Success. Image `todo-backend:latest` ready.
