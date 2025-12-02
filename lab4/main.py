import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import logging
from tokenn import TOKEN

from commands.start import router as start_router
from commands.random_photo import router as random_photo_router
from commands.search_photos import router as search_photos_router
from commands.callback_handlers import router as callback_router
from commands.history import router as history_router 

# настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    # объекты бота и диспетчера
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # регистрируем роутеры
    dp.include_router(start_router)
    dp.include_router(random_photo_router)
    dp.include_router(search_photos_router)
    dp.include_router(history_router)
    dp.include_router(callback_router)

    # команды бота
    await bot.set_my_commands([
        BotCommand(command="/start", description="старт"),
        BotCommand(command="/random_photo", description="случайная фотография"),
        BotCommand(command="/search_photos", description="поиск по ключевым словам"),
        BotCommand(command="/history", description="моя история поиска"),
        # BotCommand(command="/analyze_topic", description="анализировать тему"),
        # BotCommand(command="/settings", description="настройки"),
    ])

    print("работаеттт...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())