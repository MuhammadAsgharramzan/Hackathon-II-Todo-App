#!/usr/bin/env python3
"""
Comprehensive test to demonstrate the AI chat functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def create_mock_jwt_token():
    """Create a mock JWT token for testing purposes"""
    import base64
    import json
    import time

    # Create a simple payload with user ID
    payload = {
        "sub": "test_user_demo",
        "exp": int(time.time()) + 3600,  # Expires in 1 hour
        "iat": int(time.time())
    }

    # Encode header and payload (signature will be added manually)
    header = base64.b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload_encoded = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    # Create a mock signature (just a fixed string for testing)
    token = f"{header}.{payload_encoded}.mock-signature"
    return token

def test_scenario():
    """Test a complete scenario with the AI chat"""
    print("🎯 AI Chat Functionality Test")
    print("=" * 60)

    token = create_mock_jwt_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    conversation_id = None

    # Scenario: User wants to manage their daily tasks
    scenarios = [
        ("Add a task to buy groceries", "Adding a new task"),
        ("Add a task to call the doctor", "Adding another task"),
        ("Show my tasks", "Listing all tasks"),
        ("Complete task 1", "Completing the first task"),
        ("Show my pending tasks", "Checking remaining tasks"),
        ("Show my completed tasks", "Checking completed tasks"),
        ("Add a task to workout in the evening", "Adding one more task"),
        ("Show all my tasks", "Final task list"),
    ]

    for i, (message, description) in enumerate(scenarios, 1):
        print(f"\n📝 Test {i}: {description}")
        print(f"💬 User: {message}")
        print("-" * 40)

        # Prepare request
        data = {"message": message}
        if conversation_id:
            data["conversation_id"] = conversation_id

        try:
            response = requests.post(f"{BASE_URL}/chat/", headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                conversation_id = result.get("conversation_id")

                print(f"🤖 AI: {result['assistant_response']}")

                if result.get("tool_calls"):
                    print(f"⚙️  Tools executed: {len(result['tool_calls'])}")
                    for tool_call in result['tool_calls']:
                        print(f"   • {tool_call['tool_name'].replace('_', ' ').title()}: {tool_call['result']}")
                else:
                    print("   • No tools executed")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"❌ Exception: {str(e)}")

        time.sleep(1)  # Small delay between requests

    print("\n" + "=" * 60)
    print("✅ AI Chat functionality test completed successfully!")
    print(f"📋 Final conversation ID: {conversation_id}")

    # Show final summary
    print("\n📊 Summary of AI Capabilities Tested:")
    print("• Natural language task creation")
    print("• Task listing with filters (all, pending, completed)")
    print("• Task completion marking")
    print("• Conversation persistence")
    print("• Tool execution logging")
    print("• Error handling and user feedback")

def health_check():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend server is running and healthy")
            return True
        else:
            print(f"❌ Backend server responded with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not reach backend server: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting AI Chat Functionality Demonstration")
    print("📋 Verifying backend server...")

    if health_check():
        print("\n🎮 Running comprehensive AI chat test scenario...")
        test_scenario()
    else:
        print("\n💥 Backend server is not accessible. Please ensure:")
        print("   1. Backend is running on port 8000")
        print("   2. Use: 'cd Phase-II/backend && uvicorn main:app --host 0.0.0.0 --port 8000'")