from sqlite3 import connect
from utils.db_api.schemes import User, Withdraw, Screen, drop_User, drop_Withdraw, drop_Screen


async def db_start():

    with connect('PROTECT.db') as con:
        cursor = con.cursor()

        cursor.execute(User)
        cursor.execute(Withdraw)
        cursor.execute(Screen)

        con.commit()
        cursor.close()


async def db_drop():

    with connect('PROTECT.db') as con:
        cursor = con.cursor()

        cursor.execute(drop_User)
        cursor.execute(drop_Withdraw)
        cursor.execute(drop_Screen)

        con.commit()
        cursor.close()


