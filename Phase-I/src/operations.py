"""
Business logic for CRUD operations in the Todo Console App.
Handles all task operations with validation and error handling.
"""

import os
from typing import List, Optional, Dict, Any
from datetime import datetime

from task import Task
from storage import JSONStorage, StorageError
from config import DATE_FORMAT


class TaskOperationError(Exception):
    """Custom exception for task operation errors."""
    pass


class TaskOperations:
    """Handles all task-related operations with validation and storage management."""

    def __init__(self, storage: JSONStorage):
        """
        Initialize the task operations manager.

        Args:
            storage: JSONStorage instance for data persistence
        """
        self.storage = storage

    def _sanitize_input(self, text: str) -> str:
        """
        Sanitize input string to prevent injection and ensure safe storage.

        Args:
            text: Input string to sanitize

        Returns:
            Sanitized string
        """
        if not isinstance(text, str):
            raise ValueError("Input must be a string")

        # Remove control characters that could cause issues
        sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')

        # Strip leading/trailing whitespace
        return sanitized.strip()

    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate that task_id is a positive integer.

        Args:
            task_id: Task ID to validate

        Raises:
            ValueError: If task_id is invalid
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got {task_id}")

    def _find_task_index(self, tasks: List[Task], task_id: int) -> int:
        """
        Find the index of a task with the given ID.

        Args:
            tasks: List of tasks to search
            task_id: ID of the task to find

        Returns:
            Index of the task in the list

        Raises:
            KeyError: If task with the given ID is not found
        """
        for i, task in enumerate(tasks):
            if task.id == task_id:
                return i
        raise KeyError(f"Task with ID {task_id} not found")

    def _generate_next_id(self, tasks: List[Task]) -> int:
        """
        Generate the next available task ID.

        Args:
            tasks: Current list of tasks

        Returns:
            Next available ID
        """
        if not tasks:
            return 1
        # Find the highest ID and add 1
        max_id = max((task.id for task in tasks), default=0)
        return max_id + 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the storage.

        Args:
            title: Title of the task (required)
            description: Description of the task (optional)

        Returns:
            Created Task object

        Raises:
            ValueError: If validation fails
            TaskOperationError: If storage operation fails
        """
        # Sanitize inputs
        sanitized_title = self._sanitize_input(title)
        sanitized_description = self._sanitize_input(description)

        # Validate inputs
        if not sanitized_title:
            raise ValueError("Task title must not be empty after sanitization")

        # Load existing tasks
        try:
            tasks = self.storage.load_tasks()
        except StorageError as e:
            raise TaskOperationError(f"Failed to load tasks: {str(e)}")

        # Generate next ID
        next_id = self._generate_next_id(tasks)

        # Create new task
        new_task = Task(
            id=next_id,
            title=sanitized_title,
            description=sanitized_description,
            completed=False
        )

        # Add to tasks list and save
        tasks.append(new_task)
        try:
            self.storage.save_tasks(tasks)
        except StorageError as e:
            raise TaskOperationError(f"Failed to save task: {str(e)}")

        return new_task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks from storage, sorted by creation date (newest first).

        Returns:
            List of all Task objects, sorted by creation date (newest first)

        Raises:
            TaskOperationError: If storage operation fails
        """
        try:
            tasks = self.storage.load_tasks()
        except StorageError as e:
            raise TaskOperationError(f"Failed to load tasks: {str(e)}")

        # Sort tasks by creation date (newest first)
        # Parse the date strings and sort
        def parse_date(date_str: str) -> datetime:
            return datetime.strptime(date_str, DATE_FORMAT)

        sorted_tasks = sorted(tasks, key=lambda task: parse_date(task.created_at), reverse=True)
        return sorted_tasks

    def get_task(self, task_id: int) -> Task:
        """
        Get a specific task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object with the given ID

        Raises:
            KeyError: If task with the given ID is not found
            ValueError: If task_id is invalid
            TaskOperationError: If storage operation fails
        """
        self._validate_task_id(task_id)

        try:
            tasks = self.storage.load_tasks()
        except StorageError as e:
            raise TaskOperationError(f"Failed to load tasks: {str(e)}")

        for task in tasks:
            if task.id == task_id:
                return task

        raise KeyError(f"Task with ID {task_id} not found")

    def update_task(self, task_id: int, **kwargs) -> Task:
        """
        Update a task with the given ID.

        Args:
            task_id: ID of the task to update
            **kwargs: Fields to update (title, description, completed)

        Returns:
            Updated Task object

        Raises:
            KeyError: If task with the given ID is not found
            ValueError: If validation fails or no fields to update
            TaskOperationError: If storage operation fails
        """
        self._validate_task_id(task_id)

        # Validate and sanitize update fields
        valid_fields = {'title', 'description', 'completed'}
        invalid_fields = set(kwargs.keys()) - valid_fields
        if invalid_fields:
            raise ValueError(f"Invalid fields for update: {invalid_fields}")

        if not kwargs:
            raise ValueError("At least one field must be provided for update")

        # Sanitize string fields
        if 'title' in kwargs and kwargs['title'] is not None:
            kwargs['title'] = self._sanitize_input(str(kwargs['title']))
        if 'description' in kwargs and kwargs['description'] is not None:
            kwargs['description'] = self._sanitize_input(str(kwargs['description']))

        try:
            tasks = self.storage.load_tasks()
        except StorageError as e:
            raise TaskOperationError(f"Failed to load tasks: {str(e)}")

        # Find the task to update
        task_index = self._find_task_index(tasks, task_id)
        task = tasks[task_index]

        # Update the task properties
        for field, value in kwargs.items():
            if field == 'title' and value == "":
                raise ValueError("Task title must not be empty after sanitization")

            if hasattr(task, field):
                setattr(task, field, value)

        # Update the timestamp
        task.update_timestamp()

        # Validate the updated task
        try:
            task.validate()
        except ValueError as e:
            raise ValueError(f"Validation failed after update: {str(e)}")

        # Save the updated tasks
        try:
            self.storage.save_tasks(tasks)
        except StorageError as e:
            raise TaskOperationError(f"Failed to save updated task: {str(e)}")

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task with the given ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task was not found

        Raises:
            ValueError: If task_id is invalid
            TaskOperationError: If storage operation fails
        """
        self._validate_task_id(task_id)

        try:
            tasks = self.storage.load_tasks()
        except StorageError as e:
            raise TaskOperationError(f"Failed to load tasks: {str(e)}")

        try:
            task_index = self._find_task_index(tasks, task_id)
            tasks.pop(task_index)

            # Save the updated tasks list
            try:
                self.storage.save_tasks(tasks)
            except StorageError as e:
                raise TaskOperationError(f"Failed to save tasks after deletion: {str(e)}")

            return True
        except KeyError:
            # Task not found
            return False

    def toggle_complete(self, task_id: int) -> Task:
        """
        Toggle the completed status of a task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            Updated Task object with toggled completed status

        Raises:
            KeyError: If task with the given ID is not found
            ValueError: If task_id is invalid
            TaskOperationError: If storage operation fails
        """
        self._validate_task_id(task_id)

        try:
            tasks = self.storage.load_tasks()
        except StorageError as e:
            raise TaskOperationError(f"Failed to load tasks: {str(e)}")

        # Find the task to toggle
        task_index = self._find_task_index(tasks, task_id)
        task = tasks[task_index]

        # Toggle the completed status
        task.completed = not task.completed

        # Update the timestamp
        task.update_timestamp()

        # Save the updated tasks
        try:
            self.storage.save_tasks(tasks)
        except StorageError as e:
            raise TaskOperationError(f"Failed to save task after toggle: {str(e)}")

        return task

    def get_next_id(self) -> int:
        """
        Get the next available task ID without creating a task.

        Returns:
            Next available ID
        """
        try:
            tasks = self.storage.load_tasks()
            return self._generate_next_id(tasks)
        except StorageError:
            # If storage is inaccessible, return 1 as the next ID
            return 1