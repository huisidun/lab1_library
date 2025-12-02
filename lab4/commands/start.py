from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "помогу найти интересные фотографии или показать любую для вдохновения\n\n"
        "что я умею:\n"
        "📸 /random_photo - покажу случайную фотографию\n"
        "🔍 /search_photos + <запрос> - найду фото по ключевым словам\n"
        "🕵️ /history - покажу твою историю поисковых запросов\n\n"
        #"📊 /analyze_topic + <запрос> - покажу аналитику по вашему запросу\n\n"
        "предлагаю начать с команды: \n/random_photo "
    )
    await message.answer(welcome_text)

# для импорта в main.py
__all__ = ["router"]