#!/usr/bin/env python3
"""Simple test to check if the app components work."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from config import APP_NAME, VERSION
    print(f"✓ Config loaded: {APP_NAME} v{VERSION}")

    from task import Task
    print("✓ Task module loaded")

    # Create a test task
    test_task = Task(id=1, title="Test Task", description="A test task for verification")
    print(f"✓ Test task created: {test_task}")

    from storage import JSONStorage
    storage = JSONStorage()
    print("✓ Storage initialized")

    from operations import TaskOperations
    ops = TaskOperations(storage)
    print("✓ TaskOperations initialized")

    # Test adding a task
    new_task = ops.add_task("Test from script", "Testing if the app works")
    print(f"✓ Added test task: {new_task}")

    # Get all tasks
    all_tasks = ops.get_all_tasks()
    print(f"✓ Retrieved tasks: {len(all_tasks)} tasks found")

    print("\n🎉 All components working correctly!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()