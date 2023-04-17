
from sqlite3 import connect


async def create_withdraw(user_id: int, amount: int, photo_name: str, photo_id: str, status: str):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()
            try:
                cur.execute("INSERT INTO Withdraw VALUES(NULL, ?, ?, ?, ?, ?)",
                            (user_id, amount, photo_name, photo_id, status))
            except Exception as err:
                print(err)
            withdraw = cur.lastrowid
            db.commit()
            cur.close()
            return withdraw
    except:
        print("Не удалось создать пользователя")
        return False


async def select_withdraw(status: str = 'created'):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()
            try:
                withdraw = cur.execute("SELECT * FROM Withdraw WHERE status = '{key}'".format(key=status)).fetchone()
            except Exception as err:
                print(err)
            cur.close()
            return withdraw

    except:
        print("Не удалось найти заказ по статусу")


async def select_withdraw_by_id(withdraw_id: int):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()
            withdraw = cur.execute("SELECT * FROM Withdraw WHERE id = {key}".format(key=withdraw_id)).fetchone()
            cur.close()
            return withdraw
    except:
        print("Не удалось получить заказ по айди")
        return False


async def select_withdraw_by_user_id(user_id: int):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()
            withdraw = cur.execute("SELECT * FROM Withdraw WHERE user_id = {key}".format(key=user_id)).fetchone()
            cur.close()
        return withdraw
    except:
        print("Не удалось найти пользователя по его айди")
        return False


async def accept_withdraw(withdraw_id: int, status: str = 'accepted'):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()
            cur.execute("UPDATE Withdraw SET status = '{key}' WHERE id = {kiy}".format(key=status, kiy=withdraw_id))
            db.commit()
            cur.close()
            return True
    except:
        print("Ошибка поддтверждения")
        return False
    

async def take_amount(withdraw_id: int):
    try:
        with connect('PROTECT.db') as db:
            cur = db.cursor()

            amount = cur.execute("SELECT amount FROM Withdraw WHERE id = {key}".format(key=withdraw_id)).fetchone()
            cur.close()
            return amount
    except:
        print("Не удалось вытащить цену")
