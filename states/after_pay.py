from aiogram.dispatcher.filters.state import StatesGroup, State


class after_pay(StatesGroup):
    photo = State()
