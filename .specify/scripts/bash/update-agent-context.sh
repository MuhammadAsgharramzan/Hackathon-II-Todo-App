#!/bin/bash
# Script to update agent context with latest project information

set -e

CONTEXT_FILE=".claude/context.md"

# Create or update the context file
cat > "$CONTEXT_FILE" << EOF
# Project Context

## Project Information

- **Project Name**: Todo App Hackathon - Phase II
- **Objective**: Multi-phase todo app development with AI integration
- **Methodology**: Specification Driven Development (SDD) across four phases

## Current Status

- **Phase I**: CLI-based todo application with SDD foundation
- **Phase II**: Full-stack web application with authentication
- **Phase III**: AI agent integration with LangGraph
- **Phase IV**: Containerization and Kubernetes deployment

## Architecture Overview

- **Phase I**: CLI application with core functionality
- **Phase II**: Full-stack with FastAPI backend and Next.js frontend
- **Phase III**: AI agents with LangGraph orchestration
- **Phase IV**: Containerized deployment with Kubernetes

## Key Files

- \`Phase-I/\`: Phase I implementation
- \`Phase-II/\`: Phase II implementation
- \`Phase-III/\`: Phase III implementation
- \`Phase-IV/\`: Phase IV implementation
- \`.specify/\`: SpecifyPlus framework configuration

## Constraints

- Maintain backward compatibility where possible
- Follow security-first principles
- Ensure consistent architecture across phases
- Use SDD methodology throughout

## Dependencies

- Python 3.8+
- Node.js 16+
- specifyplus
- Docker
- Kubernetes tools

## Next Steps

- Complete Phase IV deployment
- Integrate all phases into cohesive application
- Validate cross-phase functionality
- Optimize performance and security
EOF

echo "Updated agent context file: $CONTEXT_FILE"