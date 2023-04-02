from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from utils.misc import rate_limit
from filters import IsPrivate
from utils.db_api import quick_commands as commands
from keyboards.reply_kbs import kb_menu


@rate_limit(limit=3, key='/start')
@dp.message_handler(IsPrivate(), Command("start"))
async def menu(message: types.Message):
    args = message.get_args()
    print(args)
    new_args = await commands.check_args(args, message.from_user.id)
    try:
        user = await commands.select_user(message.from_user.id)
        if user.user_id:
            await message.answer('Добро пожаловать', reply_markup=kb_menu)
    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username)
        await message.answer("Добро пожаловать")
        await message.answer("Ниже придложен наш функционал", reply_markup=kb_menu)
