from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from unsplash_client import search_photos_by_query

router = Router()

@router.message(Command("search_photos"))
async def cmd_search_photos(message: Message):
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

    if photo_data: # если не None
        await message.answer_photo(
            photo=photo_data['url'],
            caption=f"{photo_data['description']} (Фото от {photo_data['photographer']})"
        )
    else:
        await message.answer(f"Не удалось найти изображения по запросу '{query}'. Попробуйте другие ключевые слова.")

__all__ = ["router"]