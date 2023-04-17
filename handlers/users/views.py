from filters import IsPrivate
from loader import dp

from aiogram import types


@dp.message_handler(IsPrivate(), text='📢 Отзывы')
async def views(message: types.Message):
    await message.answer(f'✅Отзывы✅'
                         f'https://t.me/sale_gold_reviews')


@dp.callback_query_handler(text='sub')
async def sup_canal(call: types.CallbackQuery):
    await call.message.answer("Это ссылка на наш канал с отзывами"
                              "https://t.me/sale_gold_reviews")
