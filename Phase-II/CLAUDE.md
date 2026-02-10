# Claude Code Instructions and Guidelines

## Overview

This document provides instructions and guidelines for Claude Code agents working on this project. Claude Code is designed to assist with software engineering tasks using the SpecifyPlus framework.

## Project Context

- **Project Name**: Todo App Hackathon - Phase II
- **Objective**: Full-stack Todo app with authentication, backend (FastAPI), and frontend (Next.js)
- **Methodology**: Specification Driven Development (SDD)
- **Principles**: Security-first approach, spec-driven development

## Working with Claude Code

### Standard Commands

- `claude explain [topic]` - Get explanation about project components
- `claude help` - Get help with Claude Code usage
- `claude review [file]` - Review code for quality and standards
- `claude implement [feature]` - Implement new features following specifications

### SDD Workflow Commands

The following commands are available for the Specification Driven Development workflow:

#### Specification Commands
- `/sp.specify` - Create or update specifications
- `/sp.clarify` - Refine and clarify specifications
- `/sp.analyze` - Perform cross-artifact consistency checks

#### Planning Commands
- `/sp.plan` - Generate implementation plans
- `/sp.tasks` - Break plans into atomic tasks
- `/sp.checklist` - Generate custom checklists

#### Implementation Commands
- `/sp.implement` - Execute tasks with AI assistance
- `/sp.adr` - Document architectural decisions
- `/sp.phr` - Record prompt history

#### Governance Commands
- `/sp.constitution` - Manage project constitution
- `/sp.git.commit_pr` - Commit changes and create PRs

## Project Structure

The project follows the SpecifyPlus framework structure:

```
project-root/
├── .claude/                 # Claude Code configuration
│   └── commands/            # SDD workflow commands
├── .specify/                # SpecifyPlus framework
│   ├── memory/              # Project memory (constitution, etc.)
│   ├── scripts/             # Automation scripts
│   └── templates/           # Document templates
├── backend/                 # FastAPI backend application
├── frontend/                # Next.js frontend application
├── db/                      # Database schemas and migrations
├── specs/                   # Project specifications
├── sp.constitution.md       # Project constitution
├── sp.specify.md            # Main specification
├── sp.plan.md               # Implementation plan
└── sp.validate.md           # Validation procedures
```

## Development Guidelines

### 1. Specification First

- Always refer to specifications before implementing changes
- If specifications are unclear, use `/sp.clarify` to resolve ambiguities
- Update specifications when requirements change

### 2. Security-First Approach

- Implement authentication and authorization from the start
- Follow security best practices for API development
- Use JWT tokens for secure session management

### 3. Consistency Checks

- Regularly perform cross-artifact consistency checks
- Ensure implementation matches specifications
- Validate configurations against architecture

### 4. Documentation

- Document all architectural decisions as ADRs
- Maintain prompt history for reproducibility
- Keep specifications up-to-date

### 5. Quality Standards

- Follow the principles in the project constitution
- Ensure all APIs follow RESTful principles
- Maintain high test coverage

## Best Practices

1. **Always verify prerequisites** using the check-prerequisites script
2. **Follow the SDD workflow** for all changes
3. **Document decisions** as ADRs when making architectural choices
4. **Maintain consistency** between specifications and implementations
5. **Use automation scripts** for repetitive tasks

## Error Handling

- If encountering dependency issues, check prerequisites first
- For configuration problems, verify against the project constitution
- For implementation issues, review the relevant specifications
- Document problems and solutions as PHRs for future reference

## Getting Started

1. Review the project constitution to understand core principles
2. Examine the main specification to understand requirements
3. Use `/sp.plan` to generate an implementation plan for your task
4. Break the plan into tasks using `/sp.tasks`
5. Implement following the SDD workflow