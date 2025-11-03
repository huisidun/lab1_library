import re


def find_date(text: str) -> list:
    pattern = r'\b\d{2}\.\d{2}\.\d{4}\b'
    return re.findall(pattern, text)


def main():
    print("Введите текст, содержащий дату в формате ДД.ММ.ГГГГ:")
    user_input = input("Ваш текст: ").strip()

    if not user_input:
        print("Пустой ввод. Нечего искать.")
        return

    dates = find_date(user_input)

    if dates:
        print("\nНайдены даты (без проверки корректности):")
        for date in sorted(set(dates)):
            print(f"  - {date}")
    else:
        print("\nНичего похожего на ДД.ММ.ГГГГ не найдено.")


if __name__ == "__main__":
    main()