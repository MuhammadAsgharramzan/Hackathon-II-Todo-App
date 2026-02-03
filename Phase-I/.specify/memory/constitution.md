# Todo App Constitution – Phase I

## Core Principles

### I. Spec-Driven Development Only
All development must follow Spec-Driven Development (SDD) methodology. No code shall be written without first creating comprehensive specifications. Every feature, component, and change must have a corresponding spec document that defines requirements, constraints, and acceptance criteria.

### II. AI-Assisted Development
Claude Code shall write all production code. Human developers must not manually write implementation code. All coding tasks must be delegated to Claude Code through clear specifications and requirements. This ensures consistency, reduces human error, and maintains code quality standards.

### III. Simple Readable Python
All code must be written in simple, readable Python that follows PEP 8 guidelines. Code should prioritize clarity and maintainability over cleverness or performance optimizations (unless performance is critical). Use descriptive variable names, keep functions short and focused, and include docstrings for public APIs.

### IV. Simple Local Storage
The application must use simple local storage for data persistence. JSON file-based storage is permitted for saving task data between sessions. No external databases or complex storage systems shall be used. Data should be stored in a local JSON file at `~/.todos.json` to ensure persistence across application sessions while maintaining simplicity.

## Constraints

### Technology Constraints
- **Simple Storage Only**: Only local JSON file storage is permitted for data persistence. No relational databases, NoSQL databases, or external storage systems
- **No Web Framework**: No web frameworks (Flask, Django, FastAPI, etc.) shall be used
- **CLI Only**: The application must be a command-line interface only, with no graphical user interface
- **Single Process**: The application must run as a single process with no inter-process communication

### Implementation Constraints
- **Error Handling**: Robust error handling must be implemented for invalid inputs and edge cases
- **Input Validation**: All user inputs must be validated before processing
- **ID Management**: Special attention must be given to error handling for invalid task IDs
- **Storage Management**: The application must handle JSON file storage efficiently with proper error handling and data validation

## Development Process

### Workflow Requirements
1. **Specification First**: All features must begin with a comprehensive specification document
2. **AI Implementation**: Claude Code must implement all features based on approved specifications
3. **Testing**: Comprehensive testing must be implemented for all functionality
4. **Review**: All changes must undergo code review before being merged

### Quality Gates
- **Code Review**: All pull requests must be reviewed and approved
- **Test Coverage**: Minimum 80% test coverage required for all new features
- **Documentation**: All public APIs and complex logic must be documented
- **Spec Compliance**: Implementation must strictly follow approved specifications

## Governance

This constitution supersedes all other development practices and guidelines. All team members, including AI assistants, must comply with these principles. Amendments to this constitution require:

1. Documentation of the proposed change and rationale
2. Approval from the project architect
3. Migration plan for existing code if needed
4. Update to all dependent templates and documentation

**Version**: 1.1.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-24
