
import sys
with open('check_env_output.txt', 'w') as f:
    f.write(f"Python version: {sys.version}\n")
    try:
        import requests
        f.write(f"Requests version: {requests.__version__}\n")
    except ImportError as e:
        f.write(f"Error importing requests: {e}\n")
    except Exception as e:
        f.write(f"Unexpected error: {e}\n")
