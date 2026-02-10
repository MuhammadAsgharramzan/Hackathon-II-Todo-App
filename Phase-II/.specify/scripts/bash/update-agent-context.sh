#!/bin/bash
# Script to update agent context with latest project information

set -e

CONTEXT_FILE=".claude/context.md"

# Create or update the context file
cat > "$CONTEXT_FILE" << EOF
# Project Context

## Project Information

- **Project Name**: Todo App Hackathon - Phase II
- **Objective**: Full-stack Todo app with authentication, backend (FastAPI), and frontend (Next.js)
- **Principles**: Spec-driven development, security-first approach

## Current Status

- **Phase**: II
- **Focus**: Full-stack implementation with authentication and database integration
- **Backend**: FastAPI with JWT authentication
- **Frontend**: Next.js application
- **Database**: SQLite

## Architecture

- **Backend**: FastAPI application with authentication
- **Frontend**: Next.js application
- **Database**: SQLite
- **Authentication**: JWT-based
- **API Design**: RESTful principles

## Infrastructure Components

- **Backend Services**: API endpoints, authentication
- **Frontend Application**: User interface
- **Database**: Persistent storage
- **Security**: Authentication and authorization

## Key Files

- \`specs/\`: Project specifications
- \`backend/\`: FastAPI backend application
- \`frontend/\`: Next.js frontend application
- \`db/\`: Database schemas and migrations
- \`.specify/\`: SpecifyPlus framework configuration

## Constraints

- Follow security-first principles
- Maintain API consistency
- Ensure proper error handling
- Follow RESTful API design patterns

## Dependencies

- Python 3.8+
- Node.js 16+
- specifyplus
- FastAPI
- Next.js

## Next Steps

- Complete authentication implementation
- Connect frontend to backend APIs
- Implement database persistence
- Add comprehensive testing
EOF

echo "Updated agent context file: $CONTEXT_FILE"