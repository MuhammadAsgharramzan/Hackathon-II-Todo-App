
import sys
print(f"Python version: {sys.version}")
try:
    import requests
    print(f"Requests version: {requests.__version__}")
except ImportError as e:
    print(f"Error importing requests: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
