from filters import IsPrivate
from loader import dp

from aiogram import types


@dp.message_handler(IsPrivate(),text='📢 Отзывы')
async def views(message: types.Message):
    await message.answer(f'Это наш телеграм паблик с отзывами'
                         f'https://t.me/sale_gold_reviews')