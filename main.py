import asyncio
import logging
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram.types.web_app_info import WebAppInfo
from env.env import TOKEN as token
from keyboards.inline import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Тест", reply_markup=start_kb.as_markup())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())