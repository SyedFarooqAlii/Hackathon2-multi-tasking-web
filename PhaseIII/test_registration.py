import requests
import json

# Test the backend API endpoints
BASE_URL = "http://localhost:8000/api/v1"

print("Testing user registration and task creation...")

# 1. Try to register a test user
register_data = {
    "email": "admin@example.com",
    "password": "securepassword123"
}

print("Attempting to register a user...")
try:
    response = requests.post(f"{BASE_URL}/users/register", json=register_data)
    print(f"Registration response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        token = result.get('access_token')
        print(f"Registration successful! Got token: {token[:20]}..." if token else "No token received")

        # 2. Try to create a task with the new user
        if token:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            task_data = {
                "title": "Test Task from Admin",
                "description": "This is a test task created by the admin user"
            }

            print("Attempting to create a task...")
            response = requests.post(f"{BASE_URL}/users/me/tasks", json=task_data, headers=headers)
            print(f"Task creation response: {response.status_code}")
            if response.status_code == 200:
                task_result = response.json()
                print(f"Task created successfully: {task_result}")
            else:
                print(f"Task creation failed: {response.text}")
    else:
        print(f"Registration failed: {response.text}")
        print("Trying to login instead...")

        # Try login with default credentials if registration failed (maybe user already exists)
        login_response = requests.post(f"{BASE_URL}/users/login", json=register_data)
        print(f"Login response: {login_response.status_code}")

        if login_response.status_code == 200:
            result = login_response.json()
            token = result.get('access_token')
            print(f"Login successful! Got token: {token[:20]}..." if token else "No token received")

            if token:
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }

                task_data = {
                    "title": "Test Task from Admin",
                    "description": "This is a test task created by the admin user"
                }

                print("Attempting to create a task...")
                response = requests.post(f"{BASE_URL}/users/me/tasks", json=task_data, headers=headers)
                print(f"Task creation response: {response.status_code}")
                if response.status_code == 200:
                    task_result = response.json()
                    print(f"Task created successfully: {task_result}")
                else:
                    print(f"Task creation failed: {response.text}")

except Exception as e:
    print(f"Error during testing: {e}")