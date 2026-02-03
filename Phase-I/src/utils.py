"""
Utility functions for the Todo Console App.
Contains helper functions for common operations.
"""

import os
import sys
from typing import Any, Optional
from pathlib import Path


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause(message: str = "Press Enter to continue..."):
    """
    Pause execution and wait for user input.

    Args:
        message: Message to display to the user
    """
    input(message)


def format_datetime(datetime_str: str) -> str:
    """
    Format a datetime string for display.

    Args:
        datetime_str: Datetime string in ISO format

    Returns:
        Formatted datetime string for display
    """
    # Parse the datetime string and format it nicely
    # Input format: "2024-01-01T12:30:45"
    # Output format: "Jan 01, 2024 at 12:30 PM"
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except (ValueError, AttributeError):
        # If parsing fails, return the original string
        return datetime_str


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to a maximum length, adding ellipsis if truncated.

    Args:
        text: Text to truncate
        max_length: Maximum length of the text

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def validate_int_input(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> Optional[int]:
    """
    Get integer input from user with validation.

    Args:
        prompt: Prompt to display to the user
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)

    Returns:
        Integer value entered by user, or None if cancelled
    """
    while True:
        try:
            user_input = input(prompt).strip()

            if user_input.lower() in ['q', 'quit', 'exit']:
                return None

            value = int(user_input)

            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}")
                continue

            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}")
                continue

            return value

        except ValueError:
            print("Please enter a valid integer or 'q' to quit")


def confirm_action(message: str) -> bool:
    """
    Ask user to confirm an action.

    Args:
        message: Confirmation message

    Returns:
        True if user confirms, False otherwise
    """
    response = input(f"{message} (y/N): ").strip().lower()
    return response in ['y', 'yes', 'ye']


def ensure_directory_writable(directory: Path) -> bool:
    """
    Check if a directory is writable.

    Args:
        directory: Directory to check

    Returns:
        True if directory is writable, False otherwise
    """
    try:
        # Try to create a temporary file in the directory
        test_file = directory / ".write_test"
        test_file.touch()
        test_file.unlink()
        return True
    except (PermissionError, OSError):
        return False


def format_task_list(tasks: list) -> str:
    """
    Format a list of tasks for display.

    Args:
        tasks: List of Task objects

    Returns:
        Formatted string representation of the tasks
    """
    if not tasks:
        return "No tasks found."

    lines = []
    for task in tasks:
        status = "✓" if task.completed else "○"
        lines.append(f"  [{status}] {task.id}. {task.title}")

    return "\n".join(lines)


def colorize_status(status: bool) -> str:
    """
    Colorize task status for terminal display.

    Args:
        status: Task completion status

    Returns:
        Colorized status string
    """
    if status:
        return f"\033[92mCompleted\033[0m"  # Green
    else:
        return f"\033[91mPending\033[0m"   # Red


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to remove dangerous characters.

    Args:
        filename: Filename to sanitize

    Returns:
        Sanitized filename
    """
    # Remove potentially dangerous characters
    dangerous_chars = '<>:"/\\|?*'
    for char in dangerous_chars:
        filename = filename.replace(char, '_')

    # Limit length to prevent path issues
    if len(filename) > 255:
        filename = filename[:255]

    return filename