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

PRICE = {
    '1': [types.LabeledPrice(label='Apple Gift Card 500 ₽', amount=500*100)],
    '2': [types.LabeledPrice(label='Apple Gift Card 1500 ₽', amount=600*100)],
    '3': [types.LabeledPrice(label='Apple Gift Card 2000 ₽', amount=900*100)],
    '4': [types.LabeledPrice(label='Apple Gift Card 3000 ₽', amount=1200*100)],
    '6': [types.LabeledPrice(label='Apple Gift Card 5000 ₽', amount=1800*100)],
    '7': [types.LabeledPrice(label='Apple Gift Card 10000 ₽', amount=3000*100)],
    '8': [types.LabeledPrice(label='Apple Gift Card 1000 ₽', amount=6000*100)],
}

#prices=PRICE[f'{web_app_message.web_app_data.data}'],

@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def buy_process(web_app_message):
    content = "К сожалению, в данный момент выбранного товара нет в наличии"
    amount = (str(PRICE[f'{web_app_message.web_app_data.data}'][-1]).split("=")[-1])
    if db.check(amount = int(amount)/100):
        await bot.send_invoice(
                            chat_id=web_app_message.chat.id,
                            title='Apple Gift Card 🍏',
                            description='Подарочный сертификат Apple 🍏',
                            payload='invoiceCards',
                            currency='XTR',
                            prices=PRICE[f'{web_app_message.web_app_data.data}'],
                            )
    else:
        await bot.send_message(web_app_message.chat.id, content)



@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)
