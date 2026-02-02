from src.models.task import Task
from src.storage.manager import StorageManager


class TaskCreator:
    """Handles task creation operations."""

    def __init__(self, storage_manager: StorageManager):
        """Initialize task creator.

        Args:
            storage_manager: Storage manager instance
        """
        self.storage = storage_manager

    def add_task(self, title: str, description: str = "") -> Task:
        """Create and add a new task.

        Args:
            title: Task title (required)
            description: Task description (optional)

        Returns:
            Created Task object

        Raises:
            ValueError: If title is empty
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        # Get current tasks and next ID
        tasks = self.storage.get_all_tasks()
        next_id = self.storage.get_next_id(tasks)

        # Create new task
        new_task = Task(
            id=next_id,
            title=title.strip(),
            description=description.strip() if description else ""
        )

        # Add to list and save
        tasks.append(new_task)
        self.storage.save_tasks(tasks)

        return new_task