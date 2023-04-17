
from sqlite3 import connect


async def add_user(user_id: int, first_name: str, last_name: str, username: str, attempts: int = 0):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            cur.execute("INSERT INTO User VALUES(?, ?, ?, ?, ?, NULL)", (user_id, first_name, last_name, username, attempts))
            db.commit()
            user = cur.execute("SELECT * FROM User WHERE user_id = {key}".format(key=user_id)).fetchone()
            cur.close()
            return user
    except:
        print("Не удалось создать нового пользователя")


async def select_user(user_id: int):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            user = cur.execute("SELECT * FROM User WHERE user_id = {key}".format(key=user_id)).fetchone()
            cur.close()
            return user
    except Exception as err:
        print("Не удалось найти пользователя")
        print(err)


async def check_args(args, user_id: int):
    if args == '':
        args = '0'
        return args

    elif not args.isnumeric():
        args = '0'
        return args

    elif args.isnumeric():
        if int(args) == user_id:
            args = '0'
            return args

        elif await select_user(user_id=int(args)) is None:
            args = '0'
            return args

        else:
            args = str(args)
            return args

    else:
        args = '0'
        return args


async def select_all_users():
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            users = cur.execute("SELECT user_id FROM User").fetchall()
            cur.close()
            return users
    except:
        print("Не удалось получить айди всех пользователей")


async def select_attempt(user_id: int):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            number = cur.execute("SELECT attempts FROM User WHERE user_id = {key}".format(key=user_id)).fetchone()
            cur.close()
            return number[0]
    except:
        print("Не удалось взять попытки")
        return False


async def change_attempts(user_id: int, attempt: int):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            change = cur.execute("UPDATE User SET attempts = {kei} WHERE user_id = {key}".format(kei=attempt,
                                                                                                 key=user_id))
            cur.close()
            return True
    except:
        print("Не удалось поменять число попыток")
        return False
