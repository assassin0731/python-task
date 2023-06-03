import requests

salary_url = "http://localhost:8000/salary"

with open("token.txt", "r") as file:
    token = file.read()

headers = {"Authorization": f"Bearer {token}"}
response = requests.get(salary_url, headers=headers)

if response.status_code == 200:
    salary_data = response.json()
    print(f"Salary: {salary_data['salary']}, Next promotion date: {salary_data['next_promotion_date']}")
else:
    error_detail = response.json()["detail"]
    print(f"Error: {error_detail}")
