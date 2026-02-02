"""
Command-line interface for the Todo Console App.
Handles all user interactions and menu navigation.
"""

from typing import Optional
from operations import TaskOperations, TaskOperationError
from task import Task
from utils import clear_screen, pause, format_datetime, truncate_text, validate_int_input, confirm_action, format_task_list, colorize_status
from config import APP_NAME, VERSION


class CLI:
    """Command-line interface for the Todo Console App."""

    def __init__(self, task_ops: TaskOperations):
        """
        Initialize the CLI interface.

        Args:
            task_ops: TaskOperations instance for managing tasks
        """
        self.task_ops = task_ops

    def display_menu(self):
        """Display the main menu options."""
        clear_screen()
        print(f"\n{'='*50}")
        print(f"{APP_NAME} v{VERSION}")
        print('='*50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Complete")
        print("6. Exit")
        print('-'*50)

    def get_user_choice(self) -> int:
        """
        Get user's menu choice.

        Returns:
            Selected menu option number
        """
        while True:
            try:
                choice = validate_int_input("Enter your choice (1-6): ", min_value=1, max_value=6)
                if choice is None:  # User wants to quit
                    return 6  # Exit option
                return choice
            except ValueError:
                print("Please enter a number between 1 and 6.")
                pause()

    def add_task_flow(self):
        """Handle the add task workflow."""
        print("\n--- Add New Task ---")

        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Task title cannot be empty.")
                pause()
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            task = self.task_ops.add_task(title, description)
            print(f"\n✅ Task added successfully!")
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {truncate_text(task.description or 'None', 50)}")

        except ValueError as e:
            print(f"❌ Error: {str(e)}")
        except TaskOperationError as e:
            print(f"❌ Operation Error: {str(e)}")

        pause()

    def view_tasks_flow(self):
        """Handle the view tasks workflow."""
        print("\n--- View Tasks ---")

        try:
            tasks = self.task_ops.get_all_tasks()

            if not tasks:
                print("No tasks found.")
            else:
                print(f"\nTotal tasks: {len(tasks)}")
                print("-" * 60)

                for task in tasks:
                    status_color = colorize_status(task.completed)
                    print(f"ID: {task.id:3d} | {status_color:12s} | {task.title}")

                    if task.description:
                        print(f"       Description: {truncate_text(task.description, 60)}")

                    print(f"       Created: {format_datetime(task.created_at)}")
                    if task.created_at != task.updated_at:
                        print(f"       Updated: {format_datetime(task.updated_at)}")
                    print("-" * 60)

        except TaskOperationError as e:
            print(f"❌ Operation Error: {str(e)}")

        pause()

    def update_task_flow(self):
        """Handle the update task workflow."""
        print("\n--- Update Task ---")

        try:
            # First, show all tasks
            tasks = self.task_ops.get_all_tasks()

            if not tasks:
                print("No tasks available to update.")
                pause()
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status = "✓" if task.completed else "○"
                print(f"  [{status}] {task.id}. {task.title}")

            task_id = validate_int_input("\nEnter the task ID to update: ", min_value=1)
            if task_id is None:
                return

            # Check if task exists
            try:
                current_task = self.task_ops.get_task(task_id)
            except KeyError:
                print(f"❌ Task with ID {task_id} not found.")
                pause()
                return

            print(f"\nUpdating task: {current_task.title}")
            print("Leave blank to keep current value.")

            # Get new values (keep current if blank)
            new_title = input(f"New title (current: '{current_task.title}'): ").strip()
            if not new_title:
                new_title = current_task.title

            new_description = input(f"New description (current: '{truncate_text(current_task.description or 'None', 30)}'): ").strip()
            if new_description == "":
                new_description = current_task.description

            new_completed = input(f"Completed status (current: {'Yes' if current_task.completed else 'No'}, 'y' for yes, 'n' for no, blank to keep): ").strip().lower()
            if new_completed == "":
                new_completed = current_task.completed
            elif new_completed in ['y', 'yes']:
                new_completed = True
            elif new_completed in ['n', 'no']:
                new_completed = False
            else:
                print("Invalid input for completed status. Keeping current value.")
                new_completed = current_task.completed

            # Update the task
            updated_task = self.task_ops.update_task(
                task_id,
                title=new_title,
                description=new_description,
                completed=new_completed
            )

            print(f"\n✅ Task updated successfully!")
            print(f"ID: {updated_task.id}")
            print(f"Title: {updated_task.title}")
            print(f"Completed: {'Yes' if updated_task.completed else 'No'}")

        except ValueError as e:
            print(f"❌ Error: {str(e)}")
        except TaskOperationError as e:
            print(f"❌ Operation Error: {str(e)}")

        pause()

    def delete_task_flow(self):
        """Handle the delete task workflow."""
        print("\n--- Delete Task ---")

        try:
            # First, show all tasks
            tasks = self.task_ops.get_all_tasks()

            if not tasks:
                print("No tasks available to delete.")
                pause()
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status = "✓" if task.completed else "○"
                print(f"  [{status}] {task.id}. {task.title}")

            task_id = validate_int_input("\nEnter the task ID to delete: ", min_value=1)
            if task_id is None:
                return

            # Check if task exists
            try:
                task_to_delete = self.task_ops.get_task(task_id)
            except KeyError:
                print(f"❌ Task with ID {task_id} not found.")
                pause()
                return

            print(f"\nTask to delete: {task_to_delete.title}")

            if confirm_action("Are you sure you want to delete this task?"):
                result = self.task_ops.delete_task(task_id)

                if result:
                    print(f"\n✅ Task with ID {task_id} deleted successfully!")
                else:
                    print(f"\n❌ Task with ID {task_id} was not found.")
            else:
                print("\nDeletion cancelled.")

        except ValueError as e:
            print(f"❌ Error: {str(e)}")
        except TaskOperationError as e:
            print(f"❌ Operation Error: {str(e)}")

        pause()

    def toggle_complete_flow(self):
        """Handle the toggle complete workflow."""
        print("\n--- Toggle Task Complete ---")

        try:
            # First, show all tasks
            tasks = self.task_ops.get_all_tasks()

            if not tasks:
                print("No tasks available to toggle.")
                pause()
                return

            print("\nCurrent tasks:")
            for task in tasks:
                status = "✓" if task.completed else "○"
                print(f"  [{status}] {task.id}. {task.title}")

            task_id = validate_int_input("\nEnter the task ID to toggle: ", min_value=1)
            if task_id is None:
                return

            # Check if task exists
            try:
                current_task = self.task_ops.get_task(task_id)
            except KeyError:
                print(f"❌ Task with ID {task_id} not found.")
                pause()
                return

            # Toggle the task
            updated_task = self.task_ops.toggle_complete(task_id)
            new_status = "completed" if updated_task.completed else "pending"

            print(f"\n✅ Task '{updated_task.title}' is now {new_status}!")

        except ValueError as e:
            print(f"❌ Error: {str(e)}")
        except TaskOperationError as e:
            print(f"❌ Operation Error: {str(e)}")

        pause()

    def run(self):
        """Run the main CLI loop."""
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == 1:
                self.add_task_flow()
            elif choice == 2:
                self.view_tasks_flow()
            elif choice == 3:
                self.update_task_flow()
            elif choice == 4:
                self.delete_task_flow()
            elif choice == 5:
                self.toggle_complete_flow()
            elif choice == 6:
                print("\n👋 Thank you for using the Todo Console App!")
                break