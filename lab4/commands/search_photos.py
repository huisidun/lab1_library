from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from unsplash_client import search_photos_by_query
import os
import csv
from datetime import datetime
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

LOG_FILE = 'search_logs.csv'

router = Router()

def log_search(user_id, command, query, num_results_returned, photo_description=None, search_results_count=None, command_duration=None):
    """Сохраняет информацию о поисковом запросе в CSV."""
    try:
        file_exists = os.path.isfile(LOG_FILE)
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'timestamp', 'user_id', 'command', 'query', 'num_results_returned',
                'photo_description', 'search_results_count', 'command_duration'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'command': command,
                'query': query,
                'num_results_returned': num_results_returned,
                'photo_description': photo_description,
                'search_results_count': search_results_count,
                'command_duration': command_duration
            })
    except Exception as e:
        print(f"Ошибка при записи в search_logs: {e}")

def create_photo_keyboard(query, photo_description):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Случайное фото", callback_data="random")
        ]
    ])
    return keyboard

@router.message(Command("search_photos"))
async def cmd_search_photos(message: Message):
    start_time = time.time()

    query = message.text.split(maxsplit=1)
    if len(query) < 2:
        await message.answer("Пожалуйста, введите запрос для поиска. Пример: /search_photos котики")
        return

    query = query[1].strip()
    if not query:
        await message.answer("Пожалуйста, введите запрос для поиска. Пример: /search_photos котики")
        return

    await message.answer(f"Ищу изображение по запросу: '{query}'...")

    photo_data = search_photos_by_query(query)

    if photo_data:
        keyboard = create_photo_keyboard(query, photo_data['description'])

        await message.answer_photo(
            photo=photo_data['url'],
            caption=f"{photo_data['description']} (Фото от {photo_data['photographer']})",
            reply_markup=keyboard
        )
        command_duration = time.time() - start_time
        log_search(
            user_id=message.from_user.id,
            command='/search_photos',
            query=query,
            num_results_returned=1,
            photo_description=photo_data['description'],
            search_results_count=1,
            command_duration=command_duration
        )
    else:
        command_duration = time.time() - start_time
        await message.answer(f"Не удалось найти изображения по запросу '{query}'. Попробуйте другие ключевые слова.")
        log_search(
            user_id=message.from_user.id,
            command='/search_photos',
            query=query,
            num_results_returned=0,
            photo_description=None,
            search_results_count=0,
            command_duration=command_duration
        )

__all__ = ["router"]