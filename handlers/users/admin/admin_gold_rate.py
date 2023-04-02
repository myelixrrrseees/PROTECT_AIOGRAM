from loader import dp
from aiogram import types
from data.config import admins
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text='gold_rate', chat_id=admins, state=['*'])
async def gold_rate_(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("1 рубль - 0.67 золота")
    await state.reset_state()
