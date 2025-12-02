from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import pandas as pd
import os

LOG_FILE = 'search_logs.csv'

router = Router()

@router.message(Command("history"))
async def cmd_history(message: Message):
    user_id = message.from_user.id

    if not os.path.exists(LOG_FILE):
        await message.answer("История запросов пока недоступна.")
        return

    try:
        df = pd.read_csv(LOG_FILE)
        user_searches = df[(df['user_id'] == user_id) & (df['command'] == '/search_photos')].copy()

        if user_searches.empty:
            await message.answer("Вы пока не делали поисковых запросов.")
            return

        user_searches.sort_values(by='timestamp', ascending=False, inplace=True)

        total_searches = len(user_searches)

        last_5_queries = user_searches['query'].head(5).tolist()

        history_text = f"Ваша история поиска:\n"
        history_text += f"Всего поисковых запросов: {total_searches}\n\n"
        history_text += f"Последние 5 запросов:\n"
        for i, query in enumerate(last_5_queries, 1):
            history_text += f"{i}. {query}\n"

        await message.answer(history_text)

    except FileNotFoundError:
        await message.answer("Файл истории запросов не найден.")
    except pd.errors.EmptyDataError:
        await message.answer("Файл истории запросов пуст.")
    except Exception as e:
        await message.answer("Произошла ошибка при получении истории.")
        print(f"Ошибка в cmd_history: {e}") 

__all__ = ["router"]