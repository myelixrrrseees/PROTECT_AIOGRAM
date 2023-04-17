from aiogram.dispatcher.filters.state import StatesGroup, State


class calculator(StatesGroup):
    num_for_member = State()
    num_for_admin = State()
