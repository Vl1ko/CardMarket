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

card_summs = [
    "500",
    "1000",
    "1500",
    "2000",
    "3000",
    "5000",
    "10000"
]

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database.db'

db = Database(db_file=db_file)


@dp.message(F.text == "👨‍💻 Меню администратора")
async def admin_menu(message: types.Message):
     if (db.user_exists(message.from_user.id)):
        if (int(db.admin_exists(message.from_user.id)) == 1):
            await bot.send_message(message.chat.id, f"{message.from_user.full_name}, Вы в меню администратора.\n\nВыберите раздел",
                            reply_markup=sec_adm_keyboard)
     
@dp.message(F.text == "🛒 Действия с товарами")
async def admin_menu(message: types.Message):
     if (db.user_exists(message.from_user.id)):
        if (int(db.admin_exists(message.from_user.id)) == 1):
            await bot.send_message(message.chat.id, f"Выбраный раздел - 🛒 Действия с товарами",
                            reply_markup=card_adm_keyboard)
            
@dp.message(F.text == "🖥️ Действия с администраторами")
async def admin_menu(message: types.Message):
     if (db.user_exists(message.from_user.id)):
        if (int(db.admin_exists(message.from_user.id)) == 1):
            await bot.send_message(message.chat.id, f"Выбраный раздел - 🖥️ Действия с администраторами",
                            reply_markup=admin_adm_keyboard)

@dp.message(F.text == "📎Прочее")
async def admin_menu(message: types.Message):
     if (db.user_exists(message.from_user.id)):
        if (int(db.admin_exists(message.from_user.id)) == 1):
            await bot.send_message(message.chat.id, f"Выбраный раздел - 📎Прочее",
                            reply_markup=another_adm_keyboard)

@dp.message(F.text == "Добавить администратора")
async def cmd_admin(message: types.Message, state: FSMContext):
    if (db.user_exists(message.from_user.id)):
            if (int(db.admin_exists(message.from_user.id)) == 1):
                await message.answer(text="Введите ID нового администратора")
                await state.set_state(AdminAction.get_new_admin_id)

@dp.message(AdminAction.get_new_admin_id)
async def admin_send(message: types.Message, state: FSMContext):
    db.set_admin(user_id=message.text)
    await message.answer(text=f"Администратор c ID {message.text} добавлен")
    await state.clear()


@dp.message(F.text == "Удалить администратора")
async def cmd_admin(message: types.Message, state: FSMContext):
    if (db.user_exists(message.from_user.id)):
            if (int(db.admin_exists(message.from_user.id)) == 1):
                await message.answer(text="Введите ID администратора, которого желаете удалить")
                await state.set_state(AdminAction.get_del_admin_id)

@dp.message(AdminAction.get_del_admin_id)
async def admin_send(message: types.Message, state: FSMContext):
    db.del_admin(user_id=message.text)
    await message.answer(text=f"Администратор c ID {message.text} разжалован")
    await state.clear()


@dp.message(F.text == "Добавить карту")
async def cmd_admin(message: types.Message, state: FSMContext):
    if (db.user_exists(message.from_user.id)):
            if (int(db.admin_exists(message.from_user.id)) == 1):
                await message.answer(text="Введите номинал и номер подарочной карты через пробел\n\nНапример: 500 xxxxyyyyzzzz")
                await state.set_state(AdminAction.add_new_card)

@dp.message(AdminAction.add_new_card)
async def cmd_admin(message: types.Message, state: FSMContext):
    try:
        if ((message.text.split()[0].isdigit()) and (message.text.split()[1].isdigit())) and message.text.split()[0] in card_summs and len(message.text.split()[1])==12:
            db.add_product(amount=(message.text.split())[0], number=(message.text.split())[1])
            await message.answer(text=f"Карта номиналом {(message.text.split())[0]} с номером {(message.text.split())[1]} добавлена успешно!")
            await state.clear()
        else:
            await message.answer(text=f"Ошибка ввода!\n\nВыполнен выход из меню")
            await state.clear()
    except:
            await message.answer(text=f"Ошибка ввода!\n\nВыполнен выход из меню")
            await state.clear()


@dp.message(F.text == "Удалить карту")
async def cmd_admin(message: types.Message, state: FSMContext):
    if (db.user_exists(message.from_user.id)):
            if (int(db.admin_exists(message.from_user.id)) == 1):
                await message.answer(text="Введите номер подарочной карты, которую нужно удалить", reply_markup=None)
                await state.set_state(AdminAction.del_card)

@dp.message(AdminAction.del_card)
async def cmd_admin(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit(): 
            db.del_product(number=message.text)
            await message.answer(text=f"Карта с номером {message.text} удалена успешно!")
            await state.clear()
        else:
            await message.answer(text=f"Ошибка ввода!\n\nВыполнен выход из меню")
            await state.clear()
    except:
            await message.answer(text=f"Ошибка ввода!\n\nВыполнен выход из меню")
            await state.clear()
        


@dp.message(F.text == "⤵️ Выгрузить БД")
async def cmd_admin(message: types.Message, state: FSMContext):
    if (db.user_exists(message.from_user.id)):
            if (int(db.admin_exists(message.from_user.id)) == 1):
                await bot.send_document(message.chat.id, FSInputFile('database.db'))

@dp.message(F.text == "Тест")
async def cmd_admin(message: types.Message, state: FSMContext):
     await bot.send_message(message.chat.id, db.product_exists())


@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payment_info = str(message.successful_payment).split()
    print("\n\n\n")
    print("{:^30}".format("НОВАЯ ОПЛАТА\n\n"))
    print("{:<30}".format(f"{datetime.datetime.today()}"))
    for i in payment_info:
        print("{:<30}".format(f"{i}"))
    title1 = Bold("📱 Инструкция для iPhone, iPad или iPod touch:")
    title2 = Bold("💻 Инструкция для компьютера Mac:")
    card_number = str(db.new_buy(amount=int(int(message.successful_payment.total_amount)/119), user_id=message.chat.id, product='Подарочная карта'))
    mes = Bold(str(card_number))
    content = Text(Bold("Оплата прошла успешно!"), "🍏", "\n\nНомер подарочной карты: ", Code(mes),"\nТип товара: Подарочная карта\nСпасибо за покупку в нашем магазине будем рады видеть вас снова!\nБудем ждать ваш отзыв здесь @AppleCardss_tp\n\n", title1, "\n1. Откройте App Store.\n2. В верхней части экрана нажмите кнопку входа или свое фото.\n3. Нажмите «Погасить подарочную карту или код».\n\n", title2, "\n1. Откройте App Store.\n2. Нажмите свое имя или кнопку входа на боковой панели.\n3. Нажмите «Погасить подарочную карту».")
    await bot.send_message(message.chat.id, **content.as_kwargs())
    await bot.send_message(703656168, f"Новая покупка в боте!{datetime.datetime.today()}\n\nПользователь {message.chat.id}\n\nДанные о заказе:\n{str(message.successful_payment)}")
