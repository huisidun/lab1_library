from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "привет! я - твой фото-исследователь\n\n"
        "помогу найти интересные фотографии и даже проанализировать их\n\n"
        "что я умею:\n"
        "📸 /random_photo - покажу случайную фотографию\n"
        "🔍 /search_photos + <запрос> - найду фото по ключевым словам\n"
        "📊 /analyze_topic + <запрос> - покажу аналитику по вашему запросу\n"
        "⚙️ /settings - настрою твои предпочтения\n\n"
        "начни с команды /random_photo или просто напиши, что хочешь найти"
    )
    await message.answer(welcome_text)

# для импорта в main.py
__all__ = ["router"]