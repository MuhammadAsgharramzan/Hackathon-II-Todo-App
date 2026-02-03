"""
MCP Tools for Todo Application
These tools follow the Model Context Protocol and allow the AI agent to interact with the task management system.
"""
import logging
from typing import Optional, List, Dict, Any
from sqlmodel import Session, select
from db.database import get_session
from models.task_model import Task, TaskCreate, TaskUpdate, TaskResponse
from models.conversation_model import Conversation, Message
from auth.auth_utils import verify_token

# Configure logging for audit trails
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskTools:
    """
    MCP Tools for managing tasks in the Todo application
    """

    @staticmethod
    def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new todo task

        Parameters:
        - user_id: The ID of the user creating the task
        - title: The title of the task
        - description: Optional description of the task

        Returns:
        - task_id, status, title
        """
        try:
            # Input validation
            if not title or not title.strip():
                logger.warning(f"Invalid input for add_task: user_id={user_id}, title='{title}'")
                return {
                    "error": "Task title cannot be empty",
                    "task_id": None,
                    "status": "error",
                    "title": ""
                }

            title = title.strip()
            if description:
                description = description.strip()

            with next(get_session()) as session:
                task_create = TaskCreate(
                    title=title,
                    description=description,
                    completed=False
                )

                db_task = Task(
                    title=task_create.title,
                    description=task_create.description,
                    completed=task_create.completed,
                    user_id=user_id
                )

                session.add(db_task)
                session.commit()
                session.refresh(db_task)

                # Audit log
                logger.info(f"Task added: task_id={db_task.id}, user_id={user_id}, title='{title}'")

                return {
                    "task_id": db_task.id,
                    "status": "pending" if not db_task.completed else "completed",
                    "title": db_task.title
                }
        except Exception as e:
            logger.error(f"Error adding task for user {user_id}: {str(e)}")
            return {
                "error": f"Failed to add task: {str(e)}",
                "task_id": None,
                "status": "error",
                "title": title if 'title' in locals() else ""
            }

    @staticmethod
    def list_tasks(user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve tasks for a user

        Parameters:
        - user_id: The ID of the user whose tasks to retrieve
        - status: Optional filter ('all', 'pending', 'completed')

        Returns:
        - List of tasks
        """
        try:
            # Input validation
            if not user_id:
                logger.warning("Invalid input for list_tasks: user_id is empty")
                return []

            # Validate status parameter
            valid_statuses = [None, "all", "pending", "completed"]
            if status not in valid_statuses:
                logger.warning(f"Invalid status parameter: {status}")
                status = "all"  # Default to all

            with next(get_session()) as session:
                statement = select(Task).where(Task.user_id == user_id)

                if status and status != "all":
                    if status == "pending":
                        statement = statement.where(Task.completed == False)
                    elif status == "completed":
                        statement = statement.where(Task.completed == True)

                tasks = session.exec(statement).all()

                task_list = [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "user_id": task.user_id,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                    for task in tasks
                ]

                # Audit log
                logger.info(f"Tasks listed: user_id={user_id}, status_filter={status}, count={len(task_list)}")

                return task_list
        except Exception as e:
            logger.error(f"Error listing tasks for user {user_id}: {str(e)}")
            return []

    @staticmethod
    def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Modify a task

        Parameters:
        - user_id: The ID of the user who owns the task
        - task_id: The ID of the task to update
        - title: Optional new title
        - description: Optional new description

        Returns:
        - task_id, status, title or None if not found
        """
        try:
            # Input validation
            if not user_id:
                logger.warning(f"Invalid input for update_task: user_id is empty, task_id={task_id}")
                return None

            if task_id <= 0:
                logger.warning(f"Invalid task_id for update_task: {task_id}")
                return None

            with next(get_session()) as session:
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                db_task = session.exec(statement).first()

                if not db_task:
                    logger.warning(f"Task not found for update: task_id={task_id}, user_id={user_id}")
                    return None

                # Store original values for audit
                original_title = db_task.title
                original_description = db_task.description

                # Update task fields
                if title is not None:
                    title = title.strip()
                    if title:  # Only update if title is not empty after stripping
                        db_task.title = title
                    else:
                        logger.warning(f"Attempt to update task with empty title: task_id={task_id}")
                        return None

                if description is not None:
                    db_task.description = description.strip() if description else description

                session.add(db_task)
                session.commit()
                session.refresh(db_task)

                # Audit log
                logger.info(f"Task updated: task_id={db_task.id}, user_id={user_id}, "
                           f"title changed from '{original_title}' to '{db_task.title}'")

                return {
                    "task_id": db_task.id,
                    "status": "pending" if not db_task.completed else "completed",
                    "title": db_task.title
                }
        except Exception as e:
            logger.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
            return None

    @staticmethod
    def complete_task(user_id: str, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Mark task as completed

        Parameters:
        - user_id: The ID of the user who owns the task
        - task_id: The ID of the task to mark as completed

        Returns:
        - task_id, status, title or None if not found
        """
        try:
            # Input validation
            if not user_id:
                logger.warning(f"Invalid input for complete_task: user_id is empty, task_id={task_id}")
                return None

            if task_id <= 0:
                logger.warning(f"Invalid task_id for complete_task: {task_id}")
                return None

            with next(get_session()) as session:
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                db_task = session.exec(statement).first()

                if not db_task:
                    logger.warning(f"Task not found for completion: task_id={task_id}, user_id={user_id}")
                    return None

                if db_task.completed:
                    logger.info(f"Task already completed: task_id={task_id}, user_id={user_id}")
                    return {
                        "task_id": db_task.id,
                        "status": "completed",
                        "title": db_task.title
                    }

                db_task.completed = True
                session.add(db_task)
                session.commit()
                session.refresh(db_task)

                # Audit log
                logger.info(f"Task marked as completed: task_id={db_task.id}, user_id={user_id}")

                return {
                    "task_id": db_task.id,
                    "status": "completed",
                    "title": db_task.title
                }
        except Exception as e:
            logger.error(f"Error completing task {task_id} for user {user_id}: {str(e)}")
            return None

    @staticmethod
    def delete_task(user_id: str, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Remove a task

        Parameters:
        - user_id: The ID of the user who owns the task
        - task_id: The ID of the task to delete

        Returns:
        - task_id, status, title of the deleted task or None if not found
        """
        try:
            # Input validation
            if not user_id:
                logger.warning(f"Invalid input for delete_task: user_id is empty, task_id={task_id}")
                return None

            if task_id <= 0:
                logger.warning(f"Invalid task_id for delete_task: {task_id}")
                return None

            with next(get_session()) as session:
                statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
                db_task = session.exec(statement).first()

                if not db_task:
                    logger.warning(f"Task not found for deletion: task_id={task_id}, user_id={user_id}")
                    return None

                # Store the task details before deletion for return
                task_details = {
                    "task_id": db_task.id,
                    "status": "completed" if db_task.completed else "pending",
                    "title": db_task.title
                }

                session.delete(db_task)
                session.commit()

                # Audit log
                logger.info(f"Task deleted: task_id={db_task.id}, user_id={user_id}, title='{db_task.title}'")

                return task_details
        except Exception as e:
            logger.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
            return None