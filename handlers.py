from main import bot, dp
from keyboards import keyboard
from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import ContentType

@dp.message(Command('start'))
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Тестируем WebApp!',
                           reply_markup=keyboard)

PRICE = {
    '1': [types.LabeledPrice(label='Gift Card', amount=75000)],
    '2': [types.LabeledPrice(label='Gift Card', amount=175000)],
    '3': [types.LabeledPrice(label='Gift Card', amount=215000)],
    '4': [types.LabeledPrice(label='Gift Card', amount=315000)],
    '5': [types.LabeledPrice(label='Gift Card', amount=415000)],
    '6': [types.LabeledPrice(label='Gift Card', amount=515000)],
    '7': [types.LabeledPrice(label='Gift Card', amount=1015000)]
}

@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def buy_process(web_app_message):
    await bot.send_invoice(web_app_message.chat.id,
                           title='Подарочная карта Apple',
                           description='Подарочная карта Apple',
                           provider_token='1832575495:TEST:e246626faf7f1f0f51d66db5eb1f87c96a3b988672a574e2b3b86c17bd555880',
                           currency='rub',
                           need_email=True,
                           prices=PRICE[f'{web_app_message.web_app_data.data}'],
                           start_parameter='example',
                           payload='some_invoice')

@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


async def successful_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Платеж прошел успешно!')