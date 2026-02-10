#!/bin/bash
# Check prerequisites for the project

echo "Checking prerequisites..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.11+."
    exit 1
else
    echo "✓ Python 3 is installed: $(python3 --version)"
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install pip."
    exit 1
else
    echo "✓ pip is installed"
fi

# Check if specifyplus is installed
if ! command -v specifyplus &> /dev/null; then
    echo "specifyplus is not installed. Please install specifyplus."
    exit 1
else
    echo "✓ specifyplus is installed: $(specifyplus --version)"
fi

# Check if LangGraph components are installed
if ! python3 -c "import langgraph" &> /dev/null; then
    echo "⚠ LangGraph is not installed. Install with: pip install langgraph"
else
    echo "✓ LangGraph is installed"
fi

echo "All prerequisites are met!"