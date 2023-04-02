
from loader import dp
from data.config import admins
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text='Канал отзывов', chat_id=admins, state=['*'])
async def views(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'Прошу) '
                         f'https://t.me/sale_gold_reviews')
    await state.reset_state()