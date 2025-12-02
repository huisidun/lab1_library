from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from unsplash_client import get_random_photo_url
import os
import csv
from datetime import datetime
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

LOG_FILE = 'search_logs.csv'

router = Router()

def log_search(user_id, command, query, num_results_returned, photo_description=None, search_results_count=None, command_duration=None):
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

def create_photo_keyboard_random(photo_description):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="cлучайное фото", callback_data="random")
        ]
    ])
    return keyboard

@router.message(Command("random_photo"))
async def cmd_random_photo(message: Message):
    start_time = time.time()

    await message.answer("Ищу для вас случайное изображение...")

    photo_data = get_random_photo_url()

    if photo_data and photo_data['url']:
        keyboard = create_photo_keyboard_random(photo_data['description'])

        await message.answer_photo(
            photo=photo_data['url'],
            caption=f"{photo_data['description']} (Фото от {photo_data['photographer']})",
            reply_markup=keyboard
        )
        command_duration = time.time() - start_time
        log_search(
            user_id=message.from_user.id,
            command='/random_photo',
            query=None,
            num_results_returned=1,
            photo_description=photo_data['description'],
            search_results_count=1,
            command_duration=command_duration
        )
    else:
        command_duration = time.time() - start_time
        await message.answer("Не удалось получить изображение. Попробуйте позже.")
        log_search(
            user_id=message.from_user.id,
            command='/random_photo',
            query=None,
            num_results_returned=0,
            photo_description=None,
            search_results_count=0,
            command_duration=command_duration
        )

__all__ = ["router"]