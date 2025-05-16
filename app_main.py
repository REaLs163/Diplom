import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from app.handlers.hdl import router

# Загружаем переменные окружения
load_dotenv()

# Инициализируем бота и диспетчер для обработки работы бота
bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Запускаем роутеры для обработки хендлеров и опрос работы бота   
async def main():
    dp.include_routers(router)
    await dp.start_polling(bot, skip_updates = True)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')