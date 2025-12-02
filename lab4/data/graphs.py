import matplotlib.pyplot as plt

# гистограмма распределения голосов "за" (ups)
def plot_ups_distribution(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df['ups'], bins=30, edgecolor='black')
    plt.xlabel('Количество голосов "за"')
    plt.ylabel('Частота')
    plt.grid(axis='y')

# диаграмма рассеяния комментариев и голосов "за"
def plot_comments_vs_ups(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['num_comments'], df['ups'], alpha=0.6)
    plt.xlabel('Количество комментариев')
    plt.ylabel('Голосов "за" (ups)')
    plt.grid(True)

# столбчатую диаграмма средних ups по дням недели
def plot_avg_ups_by_day(df):
    avg_ups_by_day = df.groupby('day_of_week')['ups'].mean()
    plt.figure(figsize=(10, 6))
    avg_ups_by_day.plot(kind='bar')
    plt.xlabel('День недели (0=Пн, 6=Вс)')
    plt.ylabel('Среднее количество голосов "за"')
    plt.xticks(rotation=0)
    plt.grid(axis='y')