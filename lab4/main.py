import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import logging
from tokenn import TOKEN

from commands.start import router as start_router

# настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    # объекты бота и диспетчера
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # регистрируем роутеры
    dp.include_router(start_router)

    # команды бота
    await bot.set_my_commands([
        BotCommand(command="/start", description="старт"),
        BotCommand(command="/random_photo", description="случайная фотография"),
        BotCommand(command="/search_photos", description="поиск по ключевым словам"),
        BotCommand(command="/analyze_topic", description="анализировать тему"),
        BotCommand(command="/settings", description="настройки"),
    ])

    print("работаеттт...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())