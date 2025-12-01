import pandas as pd

df = pd.read_csv('./data/dataset.csv')

print("Первые 5 строк:")
print(df.head())

print("\nИнформация о датасете:")
print(df.info())

print("\nСтатистика по числовым признакам:")
print(df.describe())

print("\nКоличество пропущенных значений:")
print(df.isnull().sum())

print("\nНазвания столбцов:")
print(df.columns.tolist())