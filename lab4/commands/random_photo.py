from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from unsplash_client import get_random_photo_url

router = Router()

@router.message(Command("random_photo"))
async def cmd_random_photo(message: Message):
    await message.answer("Ищу для вас случайное изображение...") 

    photo_data = get_random_photo_url() 

    if photo_data and photo_data['url']:
        await message.answer_photo(
            photo=photo_data['url'],
            caption=f"{photo_data['description']} " 
            #caption=f"{photo_data['description']} (Фото от {photo_data['photographer']})" 

        )
    else:
        await message.answer("Не удалось получить изображение. Попробуйте позже.")

__all__ = ["router"]