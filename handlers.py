from main import bot, dp
from keyboards import *
from aiogram import Bot, Dispatcher, types, Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ContentType
"from aiogram.utils import executor"
from db import Database
from states import *

router = Router()

db = Database('database.db')


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
        db.add_user(message.from_user.id)
        await bot.send_message(message.chat.id, f"{message.from_user.full_name}, добро пожаловать!")

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

@dp.message(Command("add_admin"))
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


@dp.message(Command("delete_admin"))
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


@dp.message(Command("add_card"))
async def cmd_admin(message: types.Message, state: FSMContext):
    if (db.user_exists(message.from_user.id)):
            if (int(db.admin_exists(message.from_user.id)) == 1):
                await message.answer(text="Введите номинал и номер подарочной карты через пробел\n\nНапример: 500 xxxxyyyyzzzz")
                await state.set_state(AdminAction.add_new_card)

@dp.message(AdminAction.add_new_card)
async def cmd_admin(message: types.Message, state: FSMContext):
    db.add_product(amount=(message.text.split())[0], number=(message.text.split())[1])
    await message.answer(text=f"Карта номиналом {(message.text.split())[0]} с номером {(message.text.split())[1]} добавлена успешно!")
    await state.clear()

@dp.message(Command("delete_card"))
async def cmd_admin(message: types.Message, state: FSMContext):
    if (db.user_exists(message.from_user.id)):
            if (int(db.admin_exists(message.from_user.id)) == 1):
                await message.answer(text="Введите номер подарочной карты, которую нужно удалить")
                await state.set_state(AdminAction.del_card)

@dp.message(AdminAction.del_card)
async def cmd_admin(message: types.Message, state: FSMContext):
    db.del_product(number=message.text)
    await message.answer(text=f"Карта с номером {message.text} удалена успешно!")
    await state.clear()

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