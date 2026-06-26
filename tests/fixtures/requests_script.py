import requests

response = requests.get("https://httpbin.org/get")
print(f"Status: {response.status_code}")
