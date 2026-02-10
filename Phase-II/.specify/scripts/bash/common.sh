#!/bin/bash
# Common utility functions for the project

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for a condition
wait_for_condition() {
    local condition="$1"
    local timeout="${2:-60}"
    local interval="${3:-5}"

    local count=0
    while [ $count -lt $timeout ]; do
        if eval "$condition"; then
            return 0
        fi
        sleep $interval
        ((count += interval))
    done

    echo "Timeout waiting for condition: $condition"
    return 1
}

# Function to validate JSON
validate_json() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "File does not exist: $file"
        return 1
    fi

    if ! jq empty "$file" 2>/dev/null; then
        echo "Invalid JSON in file: $file"
        return 1
    fi

    return 0
}

# Function to validate YAML
validate_yaml() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "File does not exist: $file"
        return 1
    fi

    if ! python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
        echo "Invalid YAML in file: $file"
        return 1
    fi

    return 0
}

# Function to check if a Python package is installed
python_package_installed() {
    local package="$1"
    python3 -c "import $package" >/dev/null 2>&1
}

# Function to check if a Node.js package is installed
node_package_installed() {
    local package="$1"
    npm list -g "$package" >/dev/null 2>&1 || npm list "$package" >/dev/null 2>&1
}