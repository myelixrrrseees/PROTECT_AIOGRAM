from aiogram.dispatcher.filters.state import StatesGroup, State


class withdraw(StatesGroup):
    amount = State()
    photo = State()
    verify = State()