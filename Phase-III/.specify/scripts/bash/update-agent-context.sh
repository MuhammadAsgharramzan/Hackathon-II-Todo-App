#!/bin/bash
# Script to update agent context with latest project information

set -e

CONTEXT_FILE=".claude/context.md"

# Create or update the context file
cat > "$CONTEXT_FILE" << EOF
# Project Context

## Project Information

- **Project Name**: Todo App Hackathon - Phase III
- **Objective**: AI agent integration with LangGraph for enhanced task processing
- **Principles**: Ethical AI usage, spec-driven development, scalable design

## Current Status

- **Phase**: III
- **Focus**: AI agent integration with LangGraph
- **Technology**: LangGraph, AI agents for task processing
- **Integration**: Enhanced user experience through intelligent automation

## Architecture

- **AI Orchestration**: LangGraph for managing AI agent workflows
- **Task Processing**: Intelligent automation for todo tasks
- **User Interaction**: Enhanced with AI capabilities
- **Security**: Maintained with AI integration

## Infrastructure Components

- **AI Agents**: Specialized agents for different tasks
- **Workflow Engine**: LangGraph for orchestration
- **Data Processing**: AI-enhanced data handling
- **User Interface**: AI-powered interactions

## Key Files

- \`sp.constitution.md\`: Project principles and governance
- \`sp.specify.md\`: Detailed specification for AI integration
- \`sp.fix.phase-iii-auth-and-chat.md\`: Specific fixes for Phase III
- \`.specify/\`: SpecifyPlus framework configuration

## Constraints

- Maintain security standards with AI integration
- Ensure ethical AI usage
- Preserve existing functionality
- Follow responsible AI practices

## Dependencies

- Python 3.11+
- specifyplus
- LangGraph
- AI model access

## Next Steps

- Complete AI agent implementation
- Integrate with existing authentication
- Test AI workflows
- Validate against specifications
EOF

echo "Updated agent context file: $CONTEXT_FILE"