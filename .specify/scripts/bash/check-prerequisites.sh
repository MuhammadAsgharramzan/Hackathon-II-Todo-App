#!/bin/bash
# Check prerequisites for the project

echo "Checking prerequisites..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8+."
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

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 16+."
    exit 1
else
    echo "✓ Node.js is installed: $(node --version)"
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm."
    exit 1
else
    echo "✓ npm is installed: $(npm --version)"
fi

# Check if specifyplus is installed
if ! command -v specifyplus &> /dev/null; then
    echo "specifyplus is not installed. Please install specifyplus."
    exit 1
else
    echo "✓ specifyplus is installed: $(specifyplus --version)"
fi

# Check if Docker is installed (needed for Phase IV)
if ! command -v docker &> /dev/null; then
    echo "⚠ Docker is not installed. Install for Phase IV: $(docker --version 2>/dev/null || echo 'Not installed')"
else
    echo "✓ Docker is installed: $(docker --version)"
fi

# Check if kubectl is installed (needed for Phase IV)
if ! command -v kubectl &> /dev/null; then
    echo "⚠ kubectl is not installed. Install for Phase IV: $(kubectl version --client --output=yaml | grep gitVersion 2>/dev/null || echo 'Not installed')"
else
    echo "✓ kubectl is installed"
fi

echo "All prerequisites are met!"