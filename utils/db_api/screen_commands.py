
from sqlite3 import connect


async def create_screen(user_id: int, gold: float, screen_name: str, screen_id: str, status: str):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            cur.execute("INSERT INTO Screen VALUES(NULL, ?, ?, ?, ?, ?)", (user_id, gold, screen_name, screen_id, status))
            db.commit()
            screen = cur.lastrowid
            cur.close()
            return screen
    except:
        print('Скрин создан')
        return False


async def select_screen(status: str = 'created'):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            screen = cur.execute("SELECT * FROM Screen WHERE status = '{key}'".format(key=status)).fetchone()
            cur.close()
            return screen
    except:
        print("Ошибка получения скрина через статус")
        return False


async def select_screen_by_id(screen_id: int):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            screen = cur.execute("SELECT * FROM Screen WHERE id = {key}".format(key=screen_id)).fetchone()
            cur.close()
            return screen
    except:
        print("Ошибка получения скрина через айди")
        return False


async def select_screen_by_user_id(user_id: int):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            screen = cur.execute("SELECT * FROM Screen WHERE user_id = {key}".format(key=user_id)).fetchone()
            cur.close()
            return screen
    except:
        print("Ошибка получения скрина через айди пользователя")
        return False


async def accept_screen(screen_id: int, status: str = 'got'):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            cur.execute("UPDATE Screen SET status = '{key}' WHERE id = {kiy}".format(key=status, kiy=screen_id))
            db.commit()
            cur.close()
            return True
    except:
        print("Ошибка подтверждения заявки скрина")
        return False
