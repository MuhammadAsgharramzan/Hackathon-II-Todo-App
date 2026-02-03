#!/usr/bin/env python3
"""
Main entry point for the Todo Console App.
Implements the CLI interface and coordinates all components.
"""

import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from storage import JSONStorage, StorageError
from operations import TaskOperations, TaskOperationError
from cli import CLI
from config import APP_NAME, VERSION, STORAGE_PATH
from utils import ensure_directory_writable


def main():
    """Main entry point for the Todo Console App."""
    print(f"Starting {APP_NAME} v{VERSION}...")

    # Check if storage directory is writable
    storage_dir = STORAGE_PATH.parent
    if not ensure_directory_writable(storage_dir):
        print(f"❌ Error: Cannot write to storage directory: {storage_dir}")
        print("Please ensure you have write permissions to your home directory.")
        sys.exit(1)

    try:
        # Initialize storage
        storage = JSONStorage()

        # Initialize task operations
        task_ops = TaskOperations(storage)

        # Initialize CLI
        cli = CLI(task_ops)

        # Run the application
        cli.run()

    except StorageError as e:
        print(f"❌ Storage Error: {str(e)}")
        print("Please check your storage configuration and permissions.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error occurred: {str(e)}")
        print("Please contact support if the issue persists.")
        sys.exit(1)


if __name__ == "__main__":
    main()