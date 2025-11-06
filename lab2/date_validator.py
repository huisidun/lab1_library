# Поиск и валидация дат в формате ДД.ММ.ГГГГ

import re
import requests
from datetime import datetime
from typing import List


def find_potential_dates(text: str) -> List[str]:
    return re.findall(r'\b\d{2}\.\d{2}\.\d{4}\b', text)

# Проверка корректности даты через datetime
def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

# Извлечение уникальных валидных дат из текста
def extract_valid_dates_from_text(text: str) -> List[str]:
    candidates = find_potential_dates(text)
    valid_dates = [d for d in candidates if is_valid_date(d)]
    # Удаление дубликатов с сохранением порядка
    seen = set()
    result = []
    for d in valid_dates:
        if d not in seen:
            result.append(d)
            seen.add(d)
    return result

# Извлечение дат с веб-страницы (с User-Agent для совместимости)
def extract_valid_dates_from_url(url: str) -> List[str]:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Python script)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return extract_valid_dates_from_text(response.text)

# Читение файла и извлечение из него валидных дат
def extract_valid_dates_from_file(filepath: str) -> List[str]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return extract_valid_dates_from_text(f.read())