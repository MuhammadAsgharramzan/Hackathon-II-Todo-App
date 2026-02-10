#!/bin/bash
# Script to create a new Prompt History Record (PHR)

set -e

PHR_DIR=".claude/phr"
TEMPLATE_FILE=".specify/templates/phr-template.prompt.md"

# Create PHR directory if it doesn't exist
mkdir -p "$PHR_DIR"

# Get the next PHR number
next_number=$(ls "$PHR_DIR"/????-*.prompt.md 2>/dev/null | wc -l | xargs -I {} expr {} + 1)
next_number=$(printf "%04d" $next_number)

# Get PHR title from command line argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"<PHR Title>\""
    exit 1
fi

TITLE="$1"
FILENAME="$next_number-${TITLE// /-}.prompt.md"
FILENAME=${FILENAME//[^a-zA-Z0-9._-]/}

# Generate the PHR content
cat > "$PHR_DIR/$FILENAME" << EOF
# $next_number. $TITLE

Date: $(date '+%Y-%m-%d')

## Context

Provide context for the prompt and why it was needed.

## Original Prompt

\`\`\`
[Insert the original prompt here]
\`\`\`

## Response Summary

Summarize the key points from the response.

## Outcome

Describe the outcome or result achieved.

## Lessons Learned

Note any lessons learned or improvements for future prompts.
EOF

echo "Created new PHR: $PHR_DIR/$FILENAME"