import json
import os
from typing import List
from .user import User
from .stat import GameRecord
from exceptions import InvalidCredentialsError


class UserManager:
    def __init__(self, data_path: str = "data.json"):
        self.data_path = data_path
        self.users: List[User] = []
        self.records: List[GameRecord] = []
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_path):
            return

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка загрузки данных: {e}")
            return

        # Загружаем пользователя
        for raw_user in raw.get("users", []):
            try:
                self.users.append(User.from_dict(raw_user))
            except (KeyError, ValueError) as e:
                print(f"Пропущен пользователь: {e}")

        # Загружаем рекорды
        for raw_record in raw.get("stat", []):
            try:
                self.records.append(GameRecord.from_dict(raw_record))
            except (KeyError, ValueError) as e:
                print(f"Пропущен рекорд: {e}")

    def authenticate(self, phone: str, password: str) -> User:
        for user in self.users:
            if user.phone == phone and user.check_password(password):
                return user
        raise InvalidCredentialsError("Неверный телефон или пароль")

    def get_record_by_user_id(self, user_id: str) -> GameRecord:
        for record in self.records:
            if record.user_id == user_id:
                return record
        new_record = GameRecord(user_id)
        self.records.append(new_record)
        return new_record
    
    def add_user(self, user: 'User') -> bool:
        """Добавляет нового пользователя, если телефона ещё нет."""
        for existing in self.users:
            if existing.phone == user.phone:
                return False  # значит пользвоатель уже существует
        self.users.append(user)
        self._save_data()
        return True

    def _save_data(self):
        """Сохраняет пользователей и рекорды обратно в data.json."""
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, "r", encoding="utf-8") as f:
                    full_data = json.load(f)
            else:
                full_data = {"users": [], "stat": []}

            full_data["users"] = [user.to_dict() for user in self.users]
            full_data["stat"] = [record.to_dict() for record in self.records]

            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(full_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            raise