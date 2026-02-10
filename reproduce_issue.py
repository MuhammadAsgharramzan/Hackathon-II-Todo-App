import requests
import json
import random
import string

BASE_URL = "http://localhost:8000"

def get_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

# 1. Login to get token
def login():
    email = f"test_{get_random_string()}@example.com"
    password = "password123"
    username = f"user_{get_random_string()}"
    
    print(f"Attempting to register new user: {email}")
    try:
        # Register first
        reg_response = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "username": username
        })
        
        if reg_response.status_code == 200 or reg_response.status_code == 201:
            print("Registered successfully.")
        else:
            print(f"Registration failed: {reg_response.text}")
            return None

        # Then login
        print("Logging in...")
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return None
            
        return response.json()["access_token"]
    except Exception as e:
        print(f"Auth error: {e}")
        return None

# 2. Add a task
def add_task(token, title):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/tasks/", json={"title": title}, headers=headers)
    print(f"Add Task Status: {response.status_code}")
    if response.status_code == 200:
        return response.json()["id"]
    return None

# 3. Chat to delete the task by TITLE
def chat_delete_task_by_title(token, title):
    headers = {"Authorization": f"Bearer {token}"}
    message = f"delete task '{title}'"
    print(f"Sending chat message: '{message}'")
    
    response = requests.post(f"{BASE_URL}/chat/", json={
        "message": message
    }, headers=headers)
    
    print(f"Chat Response Code: {response.status_code}")
    print(f"Chat Response Body: {response.text}")

def main():
    print("Starting reproduction script...")
    token = login()
    if not token:
        print("Could not get auth token. Verify backend is running on port 8000.")
        return

    print("Got token.")
    title = "Buy Onion"
    task_id = add_task(token, title)
    if task_id:
        print(f"Created task with ID: {task_id}")
        chat_delete_task_by_title(token, title)
    else:
        print("Failed to create task.")

if __name__ == "__main__":
    main()
