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
from states import *

PRICE = {
    '1': [types.LabeledPrice(label='Apple Gift Card 500 ₽', amount=500*1.3*100)],
    '2': [types.LabeledPrice(label='Apple Gift Card 1500 ₽', amount=1500*1.3*100)],
    '3': [types.LabeledPrice(label='Apple Gift Card 2000 ₽', amount=2000*1.3*100)],
    '4': [types.LabeledPrice(label='Apple Gift Card 3000 ₽', amount=3000*1.3*100)],
    '5': [types.LabeledPrice(label='Apple Gift Card 4000 ₽', amount=4000*1.3*100)],
    '6': [types.LabeledPrice(label='Apple Gift Card 5000 ₽', amount=5000*1.3*100)],
    '7': [types.LabeledPrice(label='Apple Gift Card 10000 ₽', amount=10000*1.3*100)]
}

@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def buy_process(web_app_message):
    await bot.send_invoice(web_app_message.chat.id,
                           title='Apple Gift Card 🍏',
                           description='Подарочный сертификат Apple 🍏',
                           provider_token='1744374395:TEST:ab45a4f8517a6551e5e2',
                           currency='rub',
                           need_email=True,
                           prices=PRICE[f'{web_app_message.web_app_data.data}'],
                           start_parameter='example',
                           payload='some_invoice')

@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)
