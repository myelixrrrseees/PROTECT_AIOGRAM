from aiogram import executor
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from handlers import dp
import asyncio


class StartupMiddleware(LifetimeControllerMiddleware):
    def __init__(self, on_startup_func):
        super().__init__()
        self.on_startup_func = on_startup_func

    async def on_pre_process_update(self, update, data):
        if not self.done:
            await self.on_startup_func(dp)
            self.done = True


async def on_startup(dp):

    import middlewares
    middlewares.setup(dp)

    import filters
    filters.setup(dp)

    from utils.db_api import sqlite3

    # await sqlite3.db_drop()
    # print("DB успешно дропнута")

    await sqlite3.db_start()
    print("Таблицы успешно созданы")

    print('Готово')

    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print("Бот запущен")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    middleware = StartupMiddleware(on_startup)
    dp.middleware.setup(middleware)
    executor.start_polling(dp, on_startup=on_startup, loop=loop, skip_updates=True)
    # executor.start_polling(dp, on_startup=on_startup)
