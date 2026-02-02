import json
import os
from pathlib import Path
from typing import List, Dict, Any

from src.models.task import Task


class StorageManager:
    """Handles persistence of tasks to JSON file."""

    def __init__(self, file_path: str = None):
        """Initialize storage manager.

        Args:
            file_path: Path to JSON file (default: ~/.todos.json)
        """
        if file_path is None:
            home_dir = Path.home()
            file_path = home_dir / '.todos.json'

        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create empty file if it doesn't exist."""
        if not self.file_path.exists():
            self.file_path.touch()
            self._write_tasks([])

    def _read_file(self) -> List[Dict[str, Any]]:
        """Read and parse JSON file.

        Returns:
            List of task dictionaries
        """
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
                return json.loads(content) if content else []
        except (json.JSONDecodeError, IOError):
            return []

    def _write_tasks(self, tasks: List[Dict[str, Any]]):
        """Write tasks to JSON file.

        Args:
            tasks: List of task dictionaries to write
        """
        try:
            with open(self.file_path, 'w') as f:
                json.dump(tasks, f, indent=2)
        except IOError as e:
            raise StorageError(f"Failed to write to storage: {e}")

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from storage.

        Returns:
            List of Task objects
        """
        task_data = self._read_file()
        return [Task.from_dict(data) for data in task_data]

    def save_tasks(self, tasks: List[Task]):
        """Save list of tasks to storage.

        Args:
            tasks: List of Task objects to save
        """
        task_data = [task.to_dict() for task in tasks]
        self._write_tasks(task_data)

    def get_next_id(self, tasks: List[Task]) -> int:
        """Get the next available ID.

        Args:
            tasks: Current list of tasks

        Returns:
            Next available ID (max existing ID + 1, or 1 if no tasks)
        """
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1


class StorageError(Exception):
    """Exception raised for storage-related errors."""
    pass