from aiogram import Bot, Dispatcher
from env.env import TOKEN

import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

async def main():
    from handlers import dp
    try:
        await dp.start_polling(bot)
        print('Bot start!')
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')