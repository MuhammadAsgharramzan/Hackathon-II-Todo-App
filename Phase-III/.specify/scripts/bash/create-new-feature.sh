#!/bin/bash
# Script to create a new feature following the SDD workflow

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"<Feature Name>\""
    exit 1
fi

FEATURE_NAME="$1"
FEATURE_DIR="features/${FEATURE_NAME// /-}"
FEATURE_DIR=${FEATURE_DIR//[^a-zA-Z0-9._-]/}

# Create feature directory
mkdir -p "$FEATURE_DIR"

# Create feature specification
SPEC_FILE="$FEATURE_DIR/specification.md"
cat > "$SPEC_FILE" << EOF
# Feature Specification: $FEATURE_NAME

## Overview

Brief description of the feature and its purpose.

## Requirements

### Functional Requirements

1. Requirement 1
2. Requirement 2
3. Requirement 3

### Non-Functional Requirements

1. Performance requirement
2. Security requirement
3. Scalability requirement

## Architecture

Describe the architecture and design considerations.

## Implementation Plan

Outline the steps needed to implement this feature.

## Acceptance Criteria

Define the criteria for accepting this feature as complete.
EOF

# Create feature plan
PLAN_FILE="$FEATURE_DIR/plan.md"
cat > "$PLAN_FILE" << EOF
# Implementation Plan: $FEATURE_NAME

## Tasks

### Phase 1: Setup
- [ ] Task 1
- [ ] Task 2

### Phase 2: Development
- [ ] Task 3
- [ ] Task 4

### Phase 3: Testing
- [ ] Task 5
- [ ] Task 6

### Phase 4: Deployment
- [ ] Task 7
- [ ] Task 8
EOF

# Create feature tasks
TASKS_FILE="$FEATURE_DIR/tasks.md"
cat > "$TASKS_FILE" << EOF
# Tasks for $FEATURE_NAME

## Individual Tasks

1. **Task 1**: Description
   - Priority: High
   - Estimate: 2 hours

2. **Task 2**: Description
   - Priority: Medium
   - Estimate: 4 hours

3. **Task 3**: Description
   - Priority: Low
   - Estimate: 1 hour
EOF

echo "Created new feature: $FEATURE_NAME"
echo "Directory: $FEATURE_DIR"
echo "Files created: specification.md, plan.md, tasks.md"