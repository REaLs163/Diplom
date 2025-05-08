import asyncio
import logging
from aiogram import Bot, Dispatcher
from token_bot import TOKEN
from app.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()
   
async def main():
    dp.include_routers(router)
    await dp.start_polling(bot, skip_updates = True)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')