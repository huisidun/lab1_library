from date_validator import (
    is_valid_date,
    extract_valid_dates_from_url,
    extract_valid_dates_from_file
)


def main():
    while True:
        print("\nВыберите способ ввода даты (формат ДД.ММ.ГГГГ):")
        print("1. Ввести вручную")
        print("2. Найти даты на веб-странице (по URL)")
        print("3. Найти даты в файле")
        print("4. Выход")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            date_input = input('Введите дату в формате ДД.ММ.ГГГГ: ').strip()
            if is_valid_date(date_input):
                print('Дата корректна')
            else:
                print('Дата некорректна')
                
        elif choice == "2":
            url = input('Введите URL веб-страницы: ').strip()
            try:
                valid_dates = extract_valid_dates_from_url(url)
                if valid_dates:
                    print('Найдены корректные даты:')
                    for date in valid_dates:
                        print(f'  {date}')
                else:
                    print('Корректных дат не найдено')
            except Exception as e:
                print(f'Ошибка при обработке URL: {e}')
                
        elif choice == "3":
            file_path = input('Введите путь к файлу: ').strip()
            try:
                valid_dates = extract_valid_dates_from_file(file_path)
                if valid_dates:
                    print('Найдены корректные даты:')
                    for date in valid_dates:
                        print(f'  {date}')
                else:
                    print('Корректных дат не найдено')
            except Exception as e:
                print(f'Ошибка при чтении файла: {e}')
                
        elif choice == "4":
            print("Выход из программы")
            break
            
        else:
            print("Некорректный выбор, попробуйте снова")


if __name__ == "__main__":
    main()