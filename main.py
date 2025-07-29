import asyncio
import logging

from aiogram import Bot, Dispatcher

import handlers
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(handlers.router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')