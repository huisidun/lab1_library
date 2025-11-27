from typing import Optional


class GameRecord:
    def __init__(self, user_id: str):
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id обязателен.")
        self.user_id = user_id.strip()
        self.best_time_1: Optional[float] = None  # новичок
        self.best_time_2: Optional[float] = None  # любитель
        self.best_time_3: Optional[float] = None  # профессионал

    @classmethod
    def from_dict(cls, data: dict) -> "GameRecord":
        record = cls(data["id"])
        record.best_time_1 = cls._parse_time(data.get("best_time_1"))
        record.best_time_2 = cls._parse_time(data.get("best_time_2"))
        record.best_time_3 = cls._parse_time(data.get("best_time_3"))
        return record

    def to_dict(self) -> dict:
        return {
            "id": self.user_id,
            "best_time_1": f"{self.best_time_1:.3f}" if self.best_time_1 is not None else None,
            "best_time_2": f"{self.best_time_2:.3f}" if self.best_time_2 is not None else None,
            "best_time_3": f"{self.best_time_3:.3f}" if self.best_time_3 is not None else None,
        }

    @staticmethod
    def _parse_time(value) -> Optional[float]: 
        if value is None or value == "null":
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None