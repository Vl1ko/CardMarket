from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo


start_kb = InlineKeyboardBuilder()
start_kb.row(InlineKeyboardButton(
    text='Перейти в приложение',
    web_app=WebAppInfo(url="https://www.youtube.com"))
    )