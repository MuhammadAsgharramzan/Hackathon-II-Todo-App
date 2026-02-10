#!/bin/bash
# Script to create a new Architecture Decision Record (ADR)

set -e

ADR_DIR="docs/adrs"
TEMPLATE_FILE=".specify/templates/adr-template.md"

# Create ADR directory if it doesn't exist
mkdir -p "$ADR_DIR"

# Get the next ADR number
next_number=$(ls "$ADR_DIR"/????-*.md 2>/dev/null | wc -l | xargs -I {} expr {} + 1)
next_number=$(printf "%04d" $next_number)

# Get ADR title from command line argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"<ADR Title>\""
    exit 1
fi

TITLE="$1"
FILENAME="$next_number-${TITLE// /-}.md"
FILENAME=${FILENAME//[^a-zA-Z0-9._-]/}

# Generate the ADR content
cat > "$ADR_DIR/$FILENAME" << EOF
# $next_number. $TITLE

Date: $(date '+%Y-%m-%d')

## Status

Proposed

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

What becomes easier or more difficult to do because of this change?
EOF

echo "Created new ADR: $ADR_DIR/$FILENAME"