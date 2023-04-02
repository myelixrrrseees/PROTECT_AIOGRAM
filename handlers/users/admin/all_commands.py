from filters import IsPrivate
from loader import dp
from data.config import admins
from keyboards.inline_kbs import ikb_admin
from aiogram import types


@dp.message_handler(IsPrivate(), text='/admin', chat_id=admins, state=['*'])
async def admin_panel(message: types.Message):
    await message.answer('Твои возможности как админа', reply_markup=ikb_admin)
