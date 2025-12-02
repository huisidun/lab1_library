import pandas as pd
import matplotlib.pyplot as plt 

print("--- загрузка и изучение ---\n")

df = pd.read_csv('./data/dataset.csv')

print("Первые 5 строк:\n")
print(df.head())

print("\nИнформация о датасете:\n")
print(df.info())

print("\nСтатистика по числовым признакам:\n")
print(df.describe())

print("\nКоличество пропущенных значений:\n")
print(df.isnull().sum())

print("\nНазвания столбцов:\n")
print(df.columns.tolist())

print("\n--- подготовка датасета ---\n")

print("Преобразование 'created_utc' в формат datetime...")
df['created_at'] = pd.to_datetime(df['created_utc'], unit='s')

print("Извлечение года, месяца, дня недели...")
df['year'] = df['created_at'].dt.year
df['month'] = df['created_at'].dt.month
df['day_of_week'] = df['created_at'].dt.dayofweek

print("Создание признака 'title_length'...")
df['title_length'] = df['title'].apply(len)

print("\nСтолбцы после подготовки:")
print(df[['created_at', 'year', 'month', 'day_of_week', 'title_length']].head())

print("\n--- визуализация данных ---")

from graphs import plot_ups_distribution, plot_comments_vs_ups, plot_avg_ups_by_day

plot_ups_distribution(df)
plot_comments_vs_ups(df)
plot_avg_ups_by_day(df)

plt.show()

print("\n--- выдвижение и проверка гипотезы ---")

hypothesis = "Изображения с upvote_ratio > 0.98 получают в среднем больше комментариев, чем остальные."
print(f"Выдвинутая гипотеза: {hypothesis}")

# данные для проверки
high_ratio_posts = df[df['upvote_ratio'] > 0.98]
low_ratio_posts = df[df['upvote_ratio'] <= 0.98]

avg_comments_high_ratio = high_ratio_posts['num_comments'].mean()
avg_comments_low_ratio = low_ratio_posts['num_comments'].mean()

print(f"\nСреднее количество комментариев для постов с upvote_ratio > 0.98: {avg_comments_high_ratio:.2f}")
print(f"Среднее количество комментариев для остальных постов: {avg_comments_low_ratio:.2f}")

if avg_comments_high_ratio > avg_comments_low_ratio:
    print("\nВывод: Гипотеза ПОДТВЕРЖДАЕТСЯ. Посты с высоким upvote_ratio в среднем имеют больше комментариев.")
else:
    print("\nВывод: Гипотеза ОПРОВЕРГАЕТСЯ. Посты с высоким upvote_ratio в среднем НЕ имеют больше комментариев.")

hypothesis2 = "Есть положительная корреляция между количеством наград (total_awards_received) и голосами 'за' (ups)."
print(f"\nВыдвинутая гипотеза 2: {hypothesis2}")

correlation = df['total_awards_received'].corr(df['ups'])
print(f"Коэффициент корреляции (Pearson): {correlation:.3f}")

if correlation > 0:
    print("Вывод: Гипотеза 2 ПОДТВЕРЖДАЕТСЯ. Наблюдается положительная корреляция.")
else:
    print("Вывод: Гипотеза 2 ОПРОВЕРГАЕТСЯ. Корреляция отсутствует или отрицательна.")
