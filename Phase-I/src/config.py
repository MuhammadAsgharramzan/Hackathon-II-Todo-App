"""
Configuration and constants for the Todo Console App.
"""

import os
from pathlib import Path

# Application constants
APP_NAME = "Todo Console App"
VERSION = "1.0.0"

# File storage configuration
DEFAULT_STORAGE_FILE = ".todos.json"
STORAGE_PATH = Path.home() / DEFAULT_STORAGE_FILE

# Task validation constants
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
ALLOWED_STATUS_VALUES = ["pending", "completed", "in-progress"]

# Date format
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

# Security settings
FILE_PERMISSIONS = 0o600  # rw------- (read/write for owner only)