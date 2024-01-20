from aiogram.types import WebAppInfo
from aiogram import types

web_app = WebAppInfo(url='https://vl1ko.github.io/CardMarket/web/index.html')

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Перейти к товарам', web_app=web_app)]
    ],
    resize_keyboard=True
)

main_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='👨‍💻 Меню администратора')]
    ],
    resize_keyboard=True
)

sec_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='🛒 Действия с товарами')],
        [types.KeyboardButton(text='🖥️ Действия с администраторами')]
    ],
    resize_keyboard=True
)

card_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='/add_card')],
        [types.KeyboardButton(text='/delete_card')],
        [types.KeyboardButton(text='👨‍💻 Меню администратора')]

    ],
    resize_keyboard=True
)

admin_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='/add_admin')],
        [types.KeyboardButton(text='/delete_admin')],
        [types.KeyboardButton(text='👨‍💻 Меню администратора')]

    ],
    resize_keyboard=True
)
