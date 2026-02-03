"""
JSON storage operations with atomic writes for the Todo Console App.
Handles file-based persistence with safety measures.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from config import STORAGE_PATH, FILE_PERMISSIONS, VERSION
from task import Task


class StorageError(Exception):
    """Custom exception for storage-related errors."""
    pass


class AtomicFileWriter:
    """Context manager for atomic file writing operations."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.temp_file_path = None

    def __enter__(self):
        # Create a temporary file in the same directory as the target file
        temp_dir = self.file_path.parent
        temp_fd, temp_path_str = tempfile.mkstemp(dir=temp_dir, prefix='._temp_')

        # Close the file descriptor and wrap in Path object
        os.close(temp_fd)
        self.temp_file_path = Path(temp_path_str)
        return self.temp_file_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # If an exception occurred, remove the temporary file
            if self.temp_file_path and self.temp_file_path.exists():
                self.temp_file_path.unlink()
        else:
            # Otherwise, atomically move the temporary file to the target location
            if self.temp_file_path and self.temp_file_path.exists():
                # Move the temporary file to the final location
                self.temp_file_path.replace(self.file_path)

                # Set appropriate file permissions
                self.file_path.chmod(FILE_PERMISSIONS)


class JSONStorage:
    """Manages JSON-based storage for tasks with atomic operations."""

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the storage manager.

        Args:
            storage_path: Path to the storage file. Uses default if None.
        """
        self.storage_path = storage_path or STORAGE_PATH
        self.version = VERSION

    def _ensure_directory_exists(self):
        """Ensure the storage directory exists."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def _initialize_empty_storage(self):
        """Initialize an empty storage file."""
        self._ensure_directory_exists()
        with AtomicFileWriter(self.storage_path) as temp_path:
            data = {
                "version": self.version,
                "tasks": []
            }
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def load_tasks(self) -> List[Task]:
        """
        Load all tasks from storage.

        Returns:
            List of Task objects

        Raises:
            StorageError: If there's an issue loading the storage file
        """
        if not self.storage_path.exists():
            self._initialize_empty_storage()

        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate structure
            if not isinstance(data, dict):
                raise StorageError("Storage file contains invalid data format")

            if "tasks" not in data:
                raise StorageError("Storage file missing 'tasks' key")

            tasks_data = data["tasks"]
            if not isinstance(tasks_data, list):
                raise StorageError("'tasks' key must contain a list")

            # Convert task dictionaries to Task objects
            tasks = []
            for task_dict in tasks_data:
                if not isinstance(task_dict, dict):
                    raise StorageError(f"Invalid task data: {task_dict}")

                try:
                    task = Task.from_dict(task_dict)
                    tasks.append(task)
                except Exception as e:
                    raise StorageError(f"Failed to create Task from data {task_dict}: {str(e)}")

            return tasks

        except FileNotFoundError:
            # If file doesn't exist, initialize empty storage and return empty list
            self._initialize_empty_storage()
            return []
        except json.JSONDecodeError as e:
            raise StorageError(f"Invalid JSON in storage file: {str(e)}")
        except PermissionError:
            raise StorageError(f"Permission denied accessing storage file: {self.storage_path}")
        except OSError as e:
            raise StorageError(f"OS error accessing storage file: {str(e)}")

    def save_tasks(self, tasks: List[Task]):
        """
        Save tasks to storage with atomic operations.

        Args:
            tasks: List of Task objects to save

        Raises:
            StorageError: If there's an issue saving to the storage file
        """
        try:
            # Convert tasks to dictionaries
            tasks_data = [task.to_dict() for task in tasks]

            # Prepare storage data structure
            data = {
                "version": self.version,
                "tasks": tasks_data
            }

            # Ensure directory exists
            self._ensure_directory_exists()

            # Atomically write to storage
            with AtomicFileWriter(self.storage_path) as temp_path:
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

        except PermissionError:
            raise StorageError(f"Permission denied writing to storage file: {self.storage_path}")
        except OSError as e:
            raise StorageError(f"OS error writing to storage file: {str(e)}")
        except Exception as e:
            raise StorageError(f"Unexpected error saving tasks: {str(e)}")

    def clear_storage(self):
        """Clear all tasks from storage."""
        try:
            if self.storage_path.exists():
                self.storage_path.unlink()
            self._initialize_empty_storage()
        except Exception as e:
            raise StorageError(f"Error clearing storage: {str(e)}")