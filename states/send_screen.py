from aiogram.dispatcher.filters.state import StatesGroup, State


class send_screen(StatesGroup):
    screen = State()