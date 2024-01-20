from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class AdminAction(StatesGroup):
    get_new_admin_id = State()
    get_del_admin_id = State()
    add_new_card = State()
    del_card = State()
