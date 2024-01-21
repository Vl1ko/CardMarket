import datetime
from main import bot, dp
from keyboards import *
from aiogram import Bot, Dispatcher, types, Router
from aiogram import types, F
from aiogram.types.input_file import FSInputFile
from aiogram.utils.formatting import Text, Code, Bold
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ContentType, Message
"from aiogram.utils import executor"
from db import Database
from states import *

db = Database('database.db')

PRICE = {
    '1': [types.LabeledPrice(label='Apple Gift Card 500 ₽', amount=500*1.3*100)],
    '2': [types.LabeledPrice(label='Apple Gift Card 1500 ₽', amount=1500*1.3*100)],
    '3': [types.LabeledPrice(label='Apple Gift Card 2000 ₽', amount=2000*1.3*100)],
    '4': [types.LabeledPrice(label='Apple Gift Card 3000 ₽', amount=3000*1.3*100)],
    '5': [types.LabeledPrice(label='Apple Gift Card 4000 ₽', amount=4000*1.3*100)],
    '6': [types.LabeledPrice(label='Apple Gift Card 5000 ₽', amount=5000*1.3*100)],
    '7': [types.LabeledPrice(label='Apple Gift Card 10000 ₽', amount=10000*1.3*100)]
}



@dp.message(Command('start'))
async def start(message: types.Message):
    if (db.user_exists(message.from_user.id)):
        if (int(db.admin_exists(message.from_user.id)) == 1):
            await bot.send_message(message.chat.id, "Вы вошли в роли администратора",
                                   reply_markup=main_adm_keyboard)
        else:
            await bot.send_message(message.chat.id, f"{message.from_user.full_name}, рады снова приветствовать тебя!",
                           reply_markup=keyboard)
    else:
        db.add_user(user_id=message.from_user.id, signup=datetime.date.today())
        await bot.send_message(message.chat.id, f"{message.from_user.full_name}, добро пожаловать!")

@dp.message(Command('profile'))
async def profile(message: types.Message):
    content = Text(
        "👤 Ваш профиль:\n\n",
        "🆔 ID: ", (Code(message.from_user.id)), "\n",
        "📅 Дата регистрации: ", db.reg_date(user_id=message.from_user.id), "\n"
        "🛒 Количество покупок: ", db.bills(user_id=message.from_user.id)
    )
    await message.answer(**content.as_kwargs(), reply_markup=my_order_kb())

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
        if ((message.text.split()[0].isdigit()) and (message.text.split()[1].isdigit())):
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

@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print()
    await bot.send_message(message.chat.id, f'Платеж прошел успешно!\n\n{message.successful_payment}')