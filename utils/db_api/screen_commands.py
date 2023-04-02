import logging

from asyncpg import UniqueViolationError

from utils.db_api.schemes.screen import Screen


async def create_screen(user_id: int, screen_name: str, screen_id: str, status: str):
    try:
        screen = Screen(user_id=user_id, screen_name=screen_name, screen_id=screen_id, status=status)
        await screen.create()
        return screen.id
    except UniqueViolationError:
        print('Скрин создан')
        return False


async def select_screen(status: str = 'created'):
    screen = await Screen.query.where(Screen.status == status).gino.first()
    return screen


async def select_screen_by_id(id: int):
    screen = await Screen.query.where(Screen.id == id).gino.first()
    return screen


async def select_screen_by_user_id(user_id: int):
    screen = await Screen.query.where(Screen.user_id == user_id).gino.first()
    return screen


async def accept_screen(id: int, status: str = 'got'):
    screen = await Screen.query.where(Screen.id == id).gino.first()
    if screen:
        try:
            await screen.update(status=status).apply()
            return True
        except Exception as err:
            logging.exception(err)
    else:
        return False


async def select_screen_name_from_db(id: int):
    user = await Screen.query.where(Screen.id==id).gino.first()
    if user:
        try:
            screen = user.screen_name
            return screen
        except Exception as err:
            print(err)


async def select_screen_id_from_db(id: int):
    user = await Screen.query.where(Screen.id==id).gino.first()
    if user:
        try:
            screen = user.screen_id
            return screen
        except Exception as err:
            print(err)

