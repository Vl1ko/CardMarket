import datetime
import pathlib
import sys
from main import bot, dp
from keyboards import *
from aiogram import Bot, Dispatcher, types, Router
from aiogram import types, F
from aiogram.types.input_file import FSInputFile
from aiogram.utils.formatting import Text, Code, Bold
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ContentType, Message
from db import Database
from states import *

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database.db'

db = Database(db_file=db_file)


@dp.message(Command('start'))
async def start(message: types.Message):
    if (db.user_exists(message.from_user.id)):
        if (int(db.admin_exists(message.from_user.id)) == 1):
            await bot.send_message(message.chat.id, "Вы вошли в роли администратора",
                                   reply_markup=main_adm_keyboard)
        else:
            await bot.send_message(message.chat.id, f"{message.from_user.full_name}, рады снова приветствовать тебя!",
                                   reply_markup=mnkeyboard.as_markup(resize_keyboard=True))
    else:
        db.add_user(message.from_user.id, signup=datetime.date.today())
        await bot.send_message(message.chat.id, f"{message.from_user.full_name}, 🔥 Мы рады приветствовать вас в нашем магазине по продаже подарочных сертификатов Apple! Мы предлагаем вам множество вариаций подарочных карт на самые разные суммы!\n⚡️ После активации подарочной карты Вы сможете:\n➕ Оплачивать подписки, например Apple Music, Apple Arcade и Apple TV+\n➕ Покупать приложения, игры или делать покупки в приложениях через App Store\n➕ Покупать музыку, фильмы и многое другое в iTunes Store, приложении Apple TV или Apple Books\n➕ Платить за хранилище iCloud\nПриятных покупок 🍏",
                               reply_markup=mnkeyboard.as_markup(resize_keyboard=True))
