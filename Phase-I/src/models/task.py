from datetime import datetime
from typing import Dict, Any


class Task:
    """Represents a single task in the Todo application."""

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        """Initialize a new Task.

        Args:
            id: Unique identifier for the task
            title: Short description of the task (required)
            description: Detailed description (optional)
            completed: Current completion status (default: False)
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, title: str = None, description: str = None, completed: bool = None):
        """Update task fields and refresh updated_at timestamp.

        Args:
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed

        self.updated_at = datetime.now()

    def toggle_complete(self):
        """Toggle the completion status of the task."""
        self.completed = not self.completed
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create Task instance from dictionary.

        Args:
            data: Dictionary containing task data

        Returns:
            Task instance
        """
        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )

    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title} (ID: {self.id})"

    def __repr__(self) -> str:
        """Detailed string representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"