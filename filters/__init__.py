from aiogram import Dispatcher

from .private_chat import IsPrivate
from .database_user import IsDatabaseUser


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsDatabaseUser)
