import requests
import json

# Test the backend API endpoints
BASE_URL = "http://localhost:8000/api/v1"

print("Testing backend API...")

# 1. Test if server is reachable
try:
    response = requests.get(f"{BASE_URL}/users/me", headers={"Authorization": "Bearer invalid_token"})
    print(f"Server reachable: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Cannot connect to backend server. Is it running on port 8000?")
    exit(1)

# 2. Test without authentication (should return 401)
try:
    response = requests.get(f"{BASE_URL}/users/me/tasks")
    print(f"Unauthenticated request status: {response.status_code}")
except:
    print("Error making unauthenticated request")

# 3. Try to get all tasks (will fail without valid token)
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXItaWQiLCJleHAiOjE3MDAwMDAwMDB9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",  # Invalid token
    "Content-Type": "application/json"
}

try:
    response = requests.get(f"{BASE_URL}/users/me/tasks", headers=headers)
    print(f"Invalid token request status: {response.status_code}")
except:
    print("Error making request with invalid token")

print("\nThe issue is that you need to:")
print("1. Register a user account first")
print("2. Log in to get a valid JWT token")
print("3. Then create tasks while authenticated")
print("4. The tasks will then be associated with your user account and stored in the database")