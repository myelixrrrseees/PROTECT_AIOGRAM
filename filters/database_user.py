from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.db_api import quick_commands as commands


class IsDatabaseUser(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        print(message.from_user.id)
        user = await commands.select_user(message.from_user.id)
        return user