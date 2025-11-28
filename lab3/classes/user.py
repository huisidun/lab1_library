import re
from typing import Dict
from exceptions import InvalidUserDataError


class User:
    id: str
    first_name: str
    last_name: str
    phone: str
    email: str
    password: str

    def __init__(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        phone: str,
        email: str,
        password: str
    ):
        if not isinstance(user_id, str) or not user_id.strip():
            raise InvalidUserDataError("user_id должен быть непустой строкой")
        self.id = user_id.strip()

        if not isinstance(first_name, str) or not first_name.strip():
            raise InvalidUserDataError("first_name должен быть непустой строкой")
        self.first_name = first_name.strip()

        if not isinstance(last_name, str) or not last_name.strip():
            raise InvalidUserDataError("last_name должен быть непустой строкой")
        self.last_name = last_name.strip()

        if not isinstance(phone, str) or not self._is_valid_phone(phone):
            raise InvalidUserDataError("Некорректный формат телефона. Должен начинаться с +7 и содержать 11 цифр")
        self.phone = phone

        if not isinstance(email, str) or not self._is_valid_email(email):
            raise InvalidUserDataError("Некорректный формат email")
        self.email = email.lower()

        if not isinstance(password, str) or len(password) < 4:
            raise InvalidUserDataError("Пароль должен быть строкой не короче 4 символов")
        self.password = password

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def check_password(self, password: str) -> bool:
        return self.password == password

    def _is_valid_phone(self, phone: str) -> bool:
        return bool(re.fullmatch(r"\+7\d{10}", phone))

    def _is_valid_email(self, email: str) -> bool:
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

    def __str__(self) -> str:
        return f"Пользователь: {self.full_name} ({self.phone})"

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            user_id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            email=data["email"],
            password=data["password"]
        )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password
        }