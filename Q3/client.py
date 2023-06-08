import requests
import json

# Make a GET request to /api/v1/status
response = requests.get('http://localhost:8000/api/v1/status')
print("GET Response:")
print(response.status_code)
print(response.json())

# Make a POST request to /api/v1/status
data = {"status": "not OK"}
response = requests.post('http://localhost:8000/api/v1/status', json=data)
print("POST Response:")
print(response.status_code)
print(response.json())

# Make another GET request to /api/v1/status
response = requests.get('http://localhost:8000/api/v1/status')
print("GET Response:")
print(response.status_code)
print(response.json())

