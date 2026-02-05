#!/usr/bin/env python3
"""
Test script to verify AI chat functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
USER_ID = "test_user_123"

def create_mock_jwt_token():
    """Create a mock JWT token for testing purposes"""
    import base64
    import json

    # Create a simple payload with user ID
    payload = {
        "sub": USER_ID,
        "exp": int(time.time()) + 3600,  # Expires in 1 hour
        "iat": int(time.time())
    }

    # Encode header and payload (signature will be added manually)
    header = base64.b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload_encoded = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    # Create a mock signature (just a fixed string for testing)
    token = f"{header}.{payload_encoded}.mock-signature"
    return token

def test_ai_chat():
    """Test the AI chat functionality"""
    print("Testing AI Chat Functionality...")
    print("=" * 50)

    # Create mock JWT token
    token = create_mock_jwt_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Test cases for different AI chat functionalities
    test_messages = [
        "Add a task to buy groceries",
        "Show my tasks",
        "Add another task to call mom",
        "Complete task 1",
        "Show my completed tasks",
        "Show my pending tasks",
        "Delete task 2",
        "What can you help me with?"
    ]

    conversation_id = None

    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: {message}")
        print("-" * 30)

        # Prepare the request
        data = {
            "message": message
        }
        if conversation_id:
            data["conversation_id"] = conversation_id

        try:
            # Send request to chat endpoint
            response = requests.post(f"{BASE_URL}/chat", headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                conversation_id = result.get("conversation_id")

                print(f"Response: {result['assistant_response']}")

                if result.get("tool_calls"):
                    print(f"Tool calls executed: {len(result['tool_calls'])}")
                    for tool_call in result['tool_calls']:
                        print(f"  - {tool_call['tool_name']}: {tool_call['result']}")
                else:
                    print("  No tools executed")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the server. Please make sure the backend is running on port 8000.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

        # Small delay between requests
        time.sleep(1)

    print("\n" + "=" * 50)
    print("AI Chat functionality test completed!")

def test_health():
    """Test if the server is healthy"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Server health check passed")
            return True
        else:
            print(f"✗ Server health check failed: {response.status_code}")
            return False
    except:
        print("✗ Could not connect to server")
        return False

if __name__ == "__main__":
    print("Starting AI Chat Functionality Test")
    print("Make sure the backend server is running on port 8000")

    if test_health():
        test_ai_chat()
    else:
        print("\nThe backend server doesn't appear to be running. Please start it with:")
        print("cd Phase-II/backend && uvicorn main:app --host 0.0.0.0 --port 8000")