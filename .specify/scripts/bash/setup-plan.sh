#!/bin/bash
# Script to set up a new implementation plan

set -e

PLAN_DIR="plans"
TEMPLATE_FILE=".specify/templates/plan-template.md"

# Create plan directory if it doesn't exist
mkdir -p "$PLAN_DIR"

# Get plan title from command line argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"<Plan Title>\""
    exit 1
fi

TITLE="$1"
FILENAME="${TITLE// /_}.md"
FILENAME=${FILENAME//[^a-zA-Z0-9._-]/}

# Generate the plan content
cat > "$PLAN_DIR/$FILENAME" << EOF
# Implementation Plan: $TITLE

Date: $(date '+%Y-%m-%d')

## Overview

Brief description of the plan and its objectives.

## Scope

Define what is included and excluded from this plan.

## Objectives

1. Objective 1
2. Objective 2
3. Objective 3

## Assumptions

List any assumptions made in this plan.

## Constraints

List any constraints that may affect the plan.

## Risks

Identify potential risks and mitigation strategies.

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
|      |        |             |            |

## Resources

List required resources for plan execution.

## Timeline

| Phase | Start Date | End Date | Deliverables |
|-------|------------|----------|--------------|
|       |            |          |              |

## Success Criteria

Define how success will be measured.

## Approval

- Prepared by:
- Reviewed by:
- Approved by:
- Date:
EOF

echo "Created new plan: $PLAN_DIR/$FILENAME"