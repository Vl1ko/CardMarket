from aiogram.types import WebAppInfo
from aiogram import types

web_app = WebAppInfo(url='https://vl1ko.github.io/CardMarket/web/index.html')

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Site', web_app=web_app)]
    ],
    resize_keyboard=True
)