#Unit-тесты для модуля date_validator.py

import unittest
from date_validator import (
    is_valid_date,
    extract_valid_dates_from_text,
    extract_valid_dates_from_file
)
import os


class TestDateValidation(unittest.TestCase):

    def test_valid_dates(self):
        self.assertTrue(is_valid_date("01.01.2025"))
        self.assertTrue(is_valid_date("31.12.1999"))
        self.assertTrue(is_valid_date("29.02.2024"))  # високосный

    def test_invalid_dates(self):
        self.assertFalse(is_valid_date("32.01.2025"))
        self.assertFalse(is_valid_date("29.02.2025"))  # не високосный
        self.assertFalse(is_valid_date("31.04.2025"))  # апрель — 30 дней
        self.assertFalse(is_valid_date("00.01.2025"))
        self.assertFalse(is_valid_date("01.13.2025"))

    def test_extract_from_text(self):
        text = """
        Даты: 05.11.2025, 32.01.2025, 29.02.2024, 29.02.2025, 04.11.2025.
        Также 01.01.1000 и 31.12.9999 — допустимы.
        """
        result = extract_valid_dates_from_text(text)
        expected = ["05.11.2025", "29.02.2024", "04.11.2025", "01.01.1000", "31.12.9999"]
        self.assertEqual(result, expected)

    def test_duplicates_removed(self):
        text = "01.01.2025 и снова 01.01.2025, а также 02.02.2025."
        result = extract_valid_dates_from_text(text)
        self.assertEqual(result, ["01.01.2025", "02.02.2025"])

    def test_no_dates_found(self):
        self.assertEqual(extract_valid_dates_from_text("Просто текст."), [])

    def test_extract_from_file(self):
        # Создаём временный файл для теста
        test_content = "Корректные даты: 15.03.2020 и 29.02.2024.\nНекорректная: 31.04.2025."
        with open("temp_test_file.txt", "w", encoding="utf-8") as f:
            f.write(test_content)

        try:
            result = extract_valid_dates_from_file("temp_test_file.txt")
            self.assertEqual(result, ["15.03.2020", "29.02.2024"])
        finally:
            # Удаляем временный файл
            if os.path.exists("temp_test_file.txt"):
                os.remove("temp_test_file.txt")


if __name__ == '__main__':
    unittest.main(verbosity=2)