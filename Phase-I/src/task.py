"""
Task data model for the Todo Console App.
Implements the data structure and validation for tasks.
"""

import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict
from config import DATE_FORMAT, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH


@dataclass
class Task:
    """
    Represents a task in the Todo Console App.

    Attributes:
        id: Unique identifier for the task (auto-generated)
        title: Short description of the task (required)
        description: Detailed description (optional)
        completed: Boolean indicating if the task is completed
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        """Validate and set timestamps after initialization."""
        # Set timestamps if not provided (before validation)
        if not self.created_at:
            self.created_at = datetime.now().strftime(DATE_FORMAT)
        if not self.updated_at:
            self.updated_at = self.created_at

        self.validate()

    def validate(self):
        """Validate task attributes according to business rules."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got {self.id}")

        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Task title must be a non-empty string")

        if len(self.title.strip()) > MAX_TITLE_LENGTH:
            raise ValueError(f"Task title must not exceed {MAX_TITLE_LENGTH} characters")

        if not isinstance(self.description, str):
            raise ValueError("Task description must be a string")

        if len(self.description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Task description must not exceed {MAX_DESCRIPTION_LENGTH} characters")

        if not isinstance(self.completed, bool):
            raise ValueError("Task completed status must be a boolean")

        # Validate timestamp formats
        try:
            datetime.strptime(self.created_at, DATE_FORMAT)
            datetime.strptime(self.updated_at, DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid timestamp format. Expected ISO format YYYY-MM-DDTHH:MM:SS")

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task instance from a dictionary."""
        return cls(**data)

    def update_timestamp(self):
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now().strftime(DATE_FORMAT)

    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.title}"

    def __repr__(self) -> str:
        """Developer-friendly representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"