
import requests
import json
import time
import base64

BASE_URL = "http://localhost:8000"
USER_ID = "test_user_api_123"

def create_mock_jwt_token():
    payload = {
        "sub": USER_ID,
        "exp": int(time.time()) + 3600,
        "iat": int(time.time())
    }
    header = base64.b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload_encoded = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    token = f"{header}.{payload_encoded}.mock-signature"
    return token

def test_tasks_api():
    token = create_mock_jwt_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("Testing /tasks API...")

    # 1. Create Task
    print("\n1. Creating Task...")
    new_task = {
        "title": "API Test Task",
        "description": "Created via API test script",
        "completed": False
    }
    res = requests.post(f"{BASE_URL}/tasks/", headers=headers, json=new_task)
    if res.status_code == 200:
        task = res.json()
        print(f"Success: Created task ID {task['id']}")
        task_id = task['id']
    else:
        print(f"Failed: {res.status_code} - {res.text}")
        return

    # 2. Get Tasks
    print("\n2. Getting Tasks...")
    res = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    if res.status_code == 200:
        tasks = res.json()
        print(f"Success: Retrieved {len(tasks)} tasks")
        found = any(t['id'] == task_id for t in tasks)
        print(f"Task {task_id} found in list: {found}")
    else:
        print(f"Failed: {res.status_code} - {res.text}")

    # 3. Update Task
    print("\n3. Updating Task...")
    update_data = {"completed": True}
    res = requests.put(f"{BASE_URL}/tasks/{task_id}", headers=headers, json=update_data)
    if res.status_code == 200:
        updated_task = res.json()
        print(f"Success: Updated task completed status to {updated_task['completed']}")
    else:
        print(f"Failed: {res.status_code} - {res.text}")

    # 4. Delete Task
    print("\n4. Deleting Task...")
    res = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    if res.status_code == 200:
        print("Success: Deleted task")
    else:
        print(f"Failed: {res.status_code} - {res.text}")

    # 5. Verify Deletion
    res = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    if res.status_code == 404:
        print("Success: Task confirmed deleted (404)")
    else:
        print(f"Failed: Expected 404, got {res.status_code}")

if __name__ == "__main__":
    test_tasks_api()
