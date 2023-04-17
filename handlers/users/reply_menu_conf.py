from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from utils.misc import rate_limit
from filters import IsPrivate
from utils.db_api import quick_commands as commands
from keyboards.reply_kbs import kb_menu


async def is_subscribed(chat_id, user_id):
    chat_member = await dp.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    return chat_member.is_chat_member()


sub_kb = InlineKeyboardMarkup(row_width=1,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text="Подписаться", callback_data="sub")
                                  ]
                              ])


@rate_limit(limit=3, key='/start')
@dp.message_handler(IsPrivate(), Command("start"))
async def menu(message: types.Message):
    user_id = message.chat.id
    chat_id = "-1001401343636"
    if not await is_subscribed(chat_id, user_id):
        await message.answer("❌ Вам надо подписаться на наш канал\n\n"
                             "После того, как подпишитесь, напишите в чат /start", reply_markup=sub_kb)
        return
    args = message.get_args()
    print(args)
    new_args = await commands.check_args(args, message.from_user.id)
    try:
        user = await commands.select_user(message.from_user.id)
        if user[0]:
            await message.answer('Рады вас видеть 😊\n\n'
                                 "❗️Перед покупкой голды настоятельно рекамендуем ознакомиться с правилами ❗️", reply_markup=kb_menu)
    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username)
        await message.answer("Спасибо, что выбрали именно нас ❤️\n"
                             "Ниже показан наш функционал\n\n"
                             "❗️ Перед покупкой голды настоятельно рекамендуем ознакомиться с правилами ❗️", reply_markup=kb_menu)
