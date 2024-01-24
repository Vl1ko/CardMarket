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

script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'database.db'

db = Database(db_file=db_file)

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
    print(message.from_user.id)
    if (db.user_exists(message.from_user.id)):
        if (int(db.admin_exists(message.from_user.id)) == 1):
            await bot.send_message(message.chat.id, "Вы вошли в роли администратора",
                                   reply_markup=main_adm_keyboard)
        else:
            await bot.send_message(message.chat.id, f"{message.from_user.full_name}, рады снова приветствовать тебя!",
                           reply_markup=keyboard)
    else:
        db.add_user(message.from_user.id, signup=datetime.date.today())
        await bot.send_message(message.chat.id, f"{message.from_user.full_name}, добро пожаловать!")
        await bot.send_message(message.chat.id, f"{message.from_user.full_name}, 🔥 Мы рады приветствовать вас в нашем магазине по продаже подарочных сертификатов Apple! Мы предлагаем вам множество вариаций подарочных карт на самые разные суммы!\n⚡️ После активации подарочной карты Вы сможете:\n➕ Оплачивать подписки, например Apple Music, Apple Arcade и Apple TV+\n➕ Покупать приложения, игры или делать покупки в приложениях через App Store\n➕ Покупать музыку, фильмы и многое другое в iTunes Store, приложении Apple TV или Apple Books\n➕ Платить за хранилище iCloud\nПриятных покупок 🍏")

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
    payment_info = str(message.successful_payment).split()
    print("\n\n\n")
    print("{:^30}".format("НОВАЯ ОПЛАТА\n\n"))
    print("{:<30}".format(f"{datetime.datetime.today()}"))
    for i in payment_info:
        print("{:<30}".format(f"{i}"))
    title1 = Bold("📱 Инструкция для iPhone, iPad или iPod touch:")
    title2 = Bold("💻 Инструкция для компьютера Mac:")
    mes = Code(str(card_number))
    card_number = str(db.new_buy(amount=int(int(message.successful_payment.total_amount)/130), user_id=message.chat.id, product='Подарочная карта'))
    await bot.send_message(message.chat.id, f"Оплата прошла успешно!\nТип товара: Подарочная карта\nНомер подарочной карты : {mes}\nСпасибо за покупку в нашем магазине будем рады видеть вас снова!\nБудем ждать ваш отзыв здесь @AppleCardss\n{title1}\n1. Откройте App Store.\n2. В верхней части экрана нажмите кнопку входа или свое фото.\n3. Нажмите «Погасить подарочную карту или код».\n{Bold(title2)}\n1. Откройте App Store.\n2. Нажмите свое имя или кнопку входа на боковой панели.\n3. Нажмите «Погасить подарочную карту».")
    await bot.send_message(6165322066, f"Новая покупка в боте!{datetime.datetime.today()}\n\nПользователь {message.chat.id}\n\nДанные о заказе:\n{str(message.successful_payment)}")


@dp.callback_query(F.data == "orders")
async def history(callback: types.CallbackQuery):
    order = str(str(db.buy_history(user_id=callback.message.chat.id)).replace('[','').replace("'"," ").replace("(","").replace('"',"").replace("datetime",'').replace(",",'').replace('date','').replace(".",'').replace("|", "").replace(")","").replace("]",'').replace("'\'","").lstrip()).split()
    lenght = len(order)
    index = lenght//6
    nmes = " "
    for i in range(index):
        mes = f"{order[(6*i)]}-{order[(6*i)+1]}-{order[(6*i)+2]} {order[(6*i)+3]} {order[(6*i)+4]} {order[(6*i)+5]}\n"
        nmes = nmes + mes

    await callback.message.answer(f"История покупок в формате Дата Сумма Товар:\n\n{str(nmes)[:-2]}")