import datetime
import pathlib
import sys
from main import bot, dp
from keyboards import *
from aiogram import Bot, Dispatcher, types, Router
from aiogram import types, F
from aiogram.types.input_file import FSInputFile
from aiogram.utils.formatting import Text, Code, TextLink
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ContentType, Message
from db import Database
from states import *

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database.db'

db = Database(db_file=db_file)


@dp.message(F.text == "👤 Мой профиль")
async def profile(message: types.Message):
    content = Text(
        "👤 Ваш профиль:\n\n",
        "🆔 ID: ", (Code(message.from_user.id)), "\n",
        "📅 Дата регистрации: ", db.reg_date(user_id=message.from_user.id), "\n"
        "🛒 Количество покупок: ", db.bills(user_id=message.from_user.id)
    )
    await message.answer(**content.as_kwargs(), reply_markup=my_order_kb())

@dp.message(F.text == "📢 Перейти в канал")
async def feedback(message: types.Message):
            content = Text("Спасибо, что решил подписаться на наш ", TextLink("канал", url="https://t.me/+mmUHWUQI45Y0N2Ni"),"!")
            await message.answer(**content.as_kwargs(),
                            reply_markup=mnkeyboard.as_markup(resize_keyboard=True))

@dp.message(F.text == "👨‍💻 Тех. поддержка")
async def feedback(message: types.Message):
            content = Text("Если у Вас возникли вопросы, то Вы можете задать в их в ", TextLink("Техническую поддержку.", url="https://t.me/@applecardss_tp"),"\nОбратитие внимание, что для решение Вашего вопроса, нам может подребоваться ID вашего аккаунта (", (Code(message.from_user.id)), ")")
            await message.answer(**content.as_kwargs(),
                            reply_markup=mnkeyboard.as_markup(resize_keyboard=True))

@dp.message(F.text == "📝 Отзывы")
async def feedback(message: types.Message):
            content = Text("Если Вы хотите убедиться в честности нашего магазина, то ", TextLink("десятки положительных отзывов", url="https://t.me/+mmUHWUQI45Y0N2Ni"), " отлчино помогут Вам в этом!")
            await message.answer(**content.as_kwargs(),
                            reply_markup=mnkeyboard.as_markup(resize_keyboard=True))


@dp.callback_query(F.data == "orders")
async def history(callback: types.CallbackQuery):
    order = str(str(db.buy_history(user_id=callback.message.chat.id)).replace('[','').replace("'"," ").replace("(","").replace('"',"").replace("datetime",'').replace(",",'').replace('date','').replace(".",'').replace("|", "").replace(")","").replace("]",'').replace("'\'","").replace("\\","").lstrip()).split()
    
    lenght = len(order)
    index = lenght//7
    nmes = " "
    for i in range(index):
        mes = f"🍏 {order[(7*i)+4]} {order[(7*i)+5]} на {order[(7*i)+3]}₽ | {order[(7*i)]}.{order[(7*i)+1]}.{order[(7*i)+2]}\nКод активации: {order[(7*i)+6]}\n\n"
        nmes = nmes + mes

    await callback.message.answer(f"История покупок:\n\n{str(nmes)}")
