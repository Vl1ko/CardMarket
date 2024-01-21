from aiogram.types import WebAppInfo
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

web_app = WebAppInfo(url='https://vl1ko.github.io/CardMarket/web/index.html')
builder = InlineKeyboardBuilder()


def my_order_kb():
    order_kb = [
        [types.InlineKeyboardButton(text="🛍️ История покупок", callback_data="orders")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=order_kb)

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Перейти к товарам', web_app=web_app)]
    ],
    resize_keyboard=True
)

main_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='👨‍💻 Меню администратора')],
        [types.KeyboardButton(text='Перейти к товарам', web_app=web_app)]
    ],
    resize_keyboard=True
)

sec_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='🛒 Действия с товарами')],
        [types.KeyboardButton(text='🖥️ Действия с администраторами')],
        [types.KeyboardButton(text='📎Прочее')],
    ],
    resize_keyboard=True
)

card_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Добавить карту')],
        [types.KeyboardButton(text='Удалить карту')],
        [types.KeyboardButton(text='👨‍💻 Меню администратора')]

    ],
    resize_keyboard=True
)

admin_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Добавить администратора')],
        [types.KeyboardButton(text='Удалить администратора')],
        [types.KeyboardButton(text='👨‍💻 Меню администратора')]

    ],
    resize_keyboard=True
)

another_adm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='⤵️ Выгрузить БД')],
        [types.KeyboardButton(text='👨‍💻 Меню администратора')]

    ],
    resize_keyboard=True
)

