from aiogram import Router, types
from aiogram.types import CallbackQuery
from unsplash_client import get_random_photo_url
import logging

from .random_photo import create_photo_keyboard_random

router = Router()

@router.callback_query(lambda c: c.data == 'random')
async def process_random_callback(callback_query: CallbackQuery):
    try:
        await callback_query.answer("Ищу случайное фото...")

        photo_data = get_random_photo_url()

        if photo_data and photo_data['url']:
            keyboard = create_photo_keyboard_random(photo_data['description'])

            await callback_query.message.edit_media(
                media=types.InputMediaPhoto(media=photo_data['url'], caption=f"{photo_data['description']} (Фото от {photo_data['photographer']})"),
                reply_markup=keyboard
            )
            from .random_photo import log_search
            log_search(
                user_id=callback_query.from_user.id,
                command='/random_button',
                query=None,
                num_results_returned=1,
                photo_description=photo_data['description'],
                search_results_count=1,
                command_duration=0
            )
        else:
            await callback_query.message.edit_caption(caption="Не удалось получить изображение.", reply_markup=None)

    except Exception as e:
        await callback_query.answer("Произошла ошибка.", show_alert=True)
        logging.error(f"Ошибка при получении случайного фото: {e}")

__all__ = ["router"]