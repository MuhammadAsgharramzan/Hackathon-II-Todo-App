#!/usr/bin/env python3
"""Simple test to check if the app components work without storage."""

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

    print("\n🎉 Core modules working correctly!")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()