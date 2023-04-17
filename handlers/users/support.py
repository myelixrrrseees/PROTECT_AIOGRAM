from filters.private_chat import IsPrivate
from loader import dp
from aiogram import types


@dp.message_handler(IsPrivate(), text="🛠 Тех поддержка")
async def support(message: types.Message):
    await message.answer("По всем вопросам обращайтесь\n"
                         "@sale_gold - Администратор 🧑‍💻\n"
                         "Бесплатно Голду не даю ❗️")