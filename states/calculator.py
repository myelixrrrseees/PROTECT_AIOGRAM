from aiogram.dispatcher.filters.state import StatesGroup, State


class calculator(StatesGroup):
    num = State()
