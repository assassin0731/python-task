import requests
import sys

login_url = "http://localhost:8000/login"
username = sys.argv[1]
password = sys.argv[2]

response = requests.post(
    login_url,
    data={"username": username, "password": password}
)

if response.status_code == 200:
    token = response.json()["access_token"]
    with open("token.txt", "w") as file:
        file.write(token)
    print(f"Successfully logged in. Token: {token}")
else:
    error_detail = response.json()["detail"]
    print(f"Error: {error_detail}")
    with open("token.txt", "w") as file:
        file.write("")


