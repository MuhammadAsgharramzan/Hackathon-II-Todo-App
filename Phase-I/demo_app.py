#!/usr/bin/env python3
"""
Demonstration script for the Todo Console App.
Shows how to interact with the application programmatically.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from config import STORAGE_PATH
from storage import JSONStorage
from operations import TaskOperations
from cli import CLI

def demo_application():
    """Demonstrate the application functionality."""
    print("🎯 Todo Console App - Demonstration")
    print("="*40)

    # Initialize components
    storage = JSONStorage()
    task_ops = TaskOperations(storage)

    # Add some sample tasks
    print("\n📝 Adding sample tasks...")
    task1 = task_ops.add_task("Learn Python", "Complete Python tutorial")
    print(f"   ✓ Added: {task1}")

    task2 = task_ops.add_task("Buy groceries", "Milk, bread, eggs")
    print(f"   ✓ Added: {task2}")

    task3 = task_ops.add_task("Exercise", "Go for a 30-minute run")
    print(f"   ✓ Added: {task3}")

    # View all tasks
    print("\n📋 Viewing all tasks...")
    all_tasks = task_ops.get_all_tasks()
    for task in all_tasks:
        status = "✅" if task.completed else "⏳"
        print(f"   {status} {task.id}. {task.title} - {task.description}")

    # Toggle completion of a task
    print(f"\n🔄 Toggling completion status of task {task1.id}...")
    updated_task = task_ops.toggle_complete(task1.id)
    status = "✅ Completed" if updated_task.completed else "⏳ Pending"
    print(f"   Task '{updated_task.title}' is now {status}")

    # Update a task
    print(f"\n✏️  Updating task {task2.id}...")
    updated_task2 = task_ops.update_task(task2.id, title="Buy groceries - URGENT", completed=True)
    print(f"   ✓ Updated: {updated_task2}")

    # View tasks again to see changes
    print("\n📋 All tasks after updates:")
    all_tasks = task_ops.get_all_tasks()
    for task in all_tasks:
        status = "✅" if task.completed else "⏳"
        print(f"   {status} {task.id}. {task.title}")

    # Delete a task
    print(f"\n🗑️  Deleting task {task3.id}...")
    deleted = task_ops.delete_task(task3.id)
    if deleted:
        print(f"   ✓ Task {task3.id} deleted successfully")

    # Final view
    print("\n📋 Final task list:")
    final_tasks = task_ops.get_all_tasks()
    if final_tasks:
        for task in final_tasks:
            status = "✅" if task.completed else "⏳"
            print(f"   {status} {task.id}. {task.title}")
    else:
        print("   No tasks remaining")

    print(f"\n💾 All tasks are persisted to: {STORAGE_PATH}")
    print("\n✨ Demonstration complete!")


if __name__ == "__main__":
    demo_application()