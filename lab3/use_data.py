import json
from exceptions import InvalidCredentialsError  # тут тоже пока как наброски

def load_users() -> list:
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("users", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def authenticate_user(phone: str, password: str):
    users = load_users()
    for user in users:
        if user.get("phone") == phone and user.get("password") == password:
            return user
    raise InvalidCredentialsError("Неверный телефон или пароль")