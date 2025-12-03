import pandas as pd
import matplotlib.pyplot as plt

print("Изучение структуры и содержания датасета")

LOGS_FILE_PATH = 'search_logs.csv'

try:
    df = pd.read_csv(LOGS_FILE_PATH)
    print(f"Датасет загружен из {LOGS_FILE_PATH}")
except FileNotFoundError:
    print(f"Файл {LOGS_FILE_PATH} не найден. Пожалуйста, укажите правильный путь.")
    exit()

print("Первые 5 строк датасета:")
print(df.head())

print("\nИнформация о датасете:")
print(df.info())

print("\nСтатистика по числовым признакам:")
print(df.describe())

print("\nКоличество пропущенных значений:")
print(df.isnull().sum())

print("\nНазвания столбцов:")
print(df.columns.tolist())

print("\nПример структуры (первые 5 строк):")
print(df[['timestamp', 'user_id', 'command', 'query', 'num_results_returned', 'command_duration']].head())

print("\nВизуализыция данных")
print("Генерация графиков...")

# график 1: количество использований команд
plt.figure(figsize=(10, 6))
command_counts = df['command'].value_counts()
command_counts.plot(kind='bar')
plt.xlabel('Команда')
plt.ylabel('Количество')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show() 

# график 2: топ-10 удачных поисковых запросов
search_df = df[df['command'] == '/search_photos']
successful_searches = search_df[search_df['num_results_returned'] == 1]
success_counts = successful_searches['query'].value_counts().head(10)

if not success_counts.empty:
    plt.figure(figsize=(10, 6))
    success_counts.plot(kind='bar')
    plt.xlabel('Запрос')
    plt.ylabel('Количество успешных поисков')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show() 
else:
    print("Нет данных для построения графика удачных поисковых запросов.")

# график 3: средняя длительность выполнения команды
plt.figure(figsize=(8, 5))
avg_duration_by_command = df.groupby('command')['command_duration'].mean()
avg_duration_by_command.plot(kind='bar')
plt.xlabel('Команда')
plt.ylabel('Средняя длительность (сек)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show() 

# график 4: сравнение успешных и неуспешных поисковых запросов
search_df_viz = df[df['command'] == '/search_photos']

success_count = len(search_df_viz[search_df_viz['num_results_returned'] == 1])
failure_count = len(search_df_viz[search_df_viz['num_results_returned'] == 0])

print(f"\n--- Статистика поисковых запросов (/search_photos) ---")
print(f"Успешные запросы: {success_count}")
print(f"Неуспешные запросы: {failure_count}")

if success_count > 0 or failure_count > 0:
    plt.figure(figsize=(8, 5))
    plt.bar(['Успешные (1)', 'Неуспешные (0)'], [success_count, failure_count], color=['green', 'red'])
    plt.xlabel('Результат поиска')
    plt.ylabel('Количество запросов')
    for i, v in enumerate([success_count, failure_count]):
        plt.text(i, v + max(success_count, failure_count) * 0.01, str(v), ha='center', va='bottom')

    plt.tight_layout()
    plt.show() 
else:
    print("Нет данных для построения графика сравнения успешных/неуспешных запросов.")

print("\nПроверка гипотез")

print("\n--- Гипотеза 1: Команда /search_photos используется чаще, чем команда /random_photo ---")

command_counts_h1 = df['command'].value_counts()
search_count = command_counts_h1.get('/search_photos', 0)
random_count = command_counts_h1.get('/random_photo', 0)
button_count = command_counts_h1.get('/random_button', 0)

print(f"Команда /search_photos использовалась: {search_count} раз")
print(f"Команда /random_photo использовалась: {random_count} раз")
print(f"Кнопка 'Случайное фото' (/random_button) нажималась: {button_count} раз")
print(f"Всего запросов на случайное фото (/random_photo + /random_button): {random_count + button_count} раз")

if search_count > (random_count + button_count):
    print("Вывод: Гипотеза 1 ПОДТВЕРЖДАЕТСЯ. /search_photos используется чаще, чем случайные фото в целом.")
else:
    print("Вывод: Гипотеза 1 ОПРОВЕРГАЕТСЯ. Случайные фото запрашиваются чаще, чем /search_photos, или количества равны.")

print("\n--- Гипотеза 2: Среднее время выполнения команды /search_photos больше, чем /random_photo ---")

avg_search_duration = df[df['command'] == '/search_photos']['command_duration'].mean()
avg_random_duration = df[df['command'] == '/random_photo']['command_duration'].mean()

print(f"Средняя длительность /search_photos: {avg_search_duration:.3f} сек")
print(f"Средняя длительность /random_photo: {avg_random_duration:.3f} сек")

if avg_search_duration > avg_random_duration:
    print("Вывод: Гипотеза 2 ПОДТВЕРЖДАЕТСЯ. /search_photos выполняется дольше.")
elif avg_search_duration < avg_random_duration:
    print("Вывод: Гипотеза 2 ОПРОВЕРГАЕТСЯ. /random_photo выполняется дольше.")
else:
    print("Вывод: Гипотеза 2 ТРЕБУЕТ УТОЧНЕНИЯ. Средние времена равны.")
