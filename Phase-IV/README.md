# Todo App Hackathon - Phase IV

## Overview

This is Phase IV of the Todo App Hackathon, focusing on deploying the AI Chatbot Todo App to a local Kubernetes cluster using AI-assisted DevOps tools. The project follows a Specification Driven Development (SDD) approach with the SpecifyPlus framework.

## Project Structure

```
.
├── .claude/                        # Claude Code configuration
│   └── commands/                   # SDD workflow commands
├── .specify/                       # SpecifyPlus framework
│   ├── memory/                     # Project memory (constitution, etc.)
│   ├── scripts/                    # Automation scripts
│   │   └── bash/                   # Bash scripts
│   └── templates/                  # Document templates
├── infrastructure/                 # Infrastructure as code
│   ├── docker/                     # Docker configurations
│   ├── k8s/                        # Kubernetes configurations
│   └── minikube/                   # Minikube configurations
├── ai-agents/                      # AI agent configurations
├── deployment/                     # Deployment scripts
├── sp.constitution.md              # Project constitution
├── sp.specify.md                   # Main specification
├── sp.plan.md                      # Implementation plan
├── sp.validate.md                  # Validation procedures
├── CLAUDE.md                       # Claude Code instructions
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

## Methodology

This project follows the **Specification Driven Development (SDD)** methodology using the **SpecifyPlus framework**. The core principles include:

1. **Spec-Driven Infrastructure**: All infrastructure changes must be defined in specification documents before implementation.
2. **Agentic DevOps First**: Use AI-assisted tools (Gordon, kubectl-ai, Kagent) for all DevOps operations.
3. **No Manual Configuration**: No manual coding of Dockerfiles, Kubernetes manifests, or deployment scripts.
4. **Local Cloud-Native Parity**: Maintain identical environments from local development to production.
5. **Observability & Control**: Implement comprehensive monitoring and logging from day one.

## Getting Started

### Prerequisites

1. Install SpecifyPlus framework:
   ```bash
   pip install specifyplus
   ```

2. Verify installation:
   ```bash
   specifyplus --version
   ```

3. Run prerequisite check:
   ```bash
   bash .specify/scripts/bash/check-prerequisites.sh
   ```

### SDD Workflow Commands

The project includes several Claude Code commands for the SDD workflow:

- `/sp.specify` - Create or update specifications
- `/sp.plan` - Generate implementation plans
- `/sp.tasks` - Break plans into atomic tasks
- `/sp.implement` - Execute tasks with AI assistance
- `/sp.adr` - Document architectural decisions
- `/sp.constitution` - Manage project constitution
- `/sp.analyze` - Perform cross-artifact consistency checks

### Quick Start

1. Review the project constitution: `sp.constitution.md`
2. Examine the main specification: `sp.specify.md`
3. Use the SDD commands to work on the project following the workflow

## Components

### Existing Components

- **Backend**: FastAPI application with AI agents
- **Frontend**: Next.js application
- **Database**: SQLite
- **Authentication**: JWT-based
- **AI Integration**: LangGraph agents for task processing

### Infrastructure Components

- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Local Cluster**: Minikube
- **Deployment Strategy**: Declarative, spec-driven

## AI-Assisted DevOps Tools

This project uses the following AI-assisted DevOps tools:

- **Gordon**: For Docker containerization
- **kubectl-ai**: For Kubernetes operations
- **Kagent**: For automation

These tools align with the "agentic DevOps first" approach and eliminate the need for manual configuration coding.

## Contributing

Follow the Specification Driven Development workflow:

1. Define requirements in specifications
2. Generate implementation plans
3. Break plans into tasks
4. Implement using AI assistance
5. Validate against specifications
6. Document architectural decisions