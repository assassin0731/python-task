from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import hashlib
import csv

with open('users.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
employees = {}
for row in data:
    inner_dict = {"password": row[1],
                  "salary": row[2],
                  "next_promotion_date": row[3]}
    employees[row[0]] = inner_dict


app = FastAPI()

# Секретный ключ для подписи токенов (можно генерировать случайную строку)
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Определение функции для проверки аутентификации пользователя
def authenticate(username: str, password: str):
    if username in employees and employees[username]["password"] == password:
        return True
    else:
        return False


# Определение функции для генерации токена
def create_access_token(username: str):
    expires_delta = timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    token = f"{username}:{expire.timestamp()}:{hashlib.sha256(f'{username}{expire.timestamp()}{SECRET_KEY}'.encode('utf-8')).hexdigest()}"
    return token


# Определение функции, проверяющей валидность полученного токена и получающей пользователя
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login"))):
    try:
        username, expire_timestamp, _ = token.split(":")
        expire = datetime.fromtimestamp(float(expire_timestamp))
        if datetime.utcnow() > expire:
            raise HTTPException(status_code=401, detail="Token expired")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")
    return username


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Определение роута для аутентификации, возвращает токен при успешной аутентификации
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if not authenticate(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(username)
    return {"access_token": access_token, "token_type": "bearer"}


# Определение роута для получения информации о зарплате и дате следующего повышения
@app.get("/salary")
async def read_salary(current_user: str = Depends(get_current_user)):
    salary = employees[current_user]["salary"]
    next_promotion_date = employees[current_user]["next_promotion_date"]
    return {"salary": salary, "next_promotion_date": next_promotion_date}
