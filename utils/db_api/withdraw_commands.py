import logging

from asyncpg import UniqueViolationError

import sqlite3 as sql
from utils.db_api.schemes.withdraw import Withdraw


async def create_withdraw(user_id: int, amount: int, photo_name: str, photo_id: str, status: str):
    try:
        withdraw = Withdraw(user_id=user_id, amount=amount, photo_name=photo_name, photo_id=photo_id, status=status)
        await withdraw.create()
        return withdraw.id
    except UniqueViolationError:
        print('Выплата не создана')
        return False


async def select_withdraw(status: str = 'created'):
    try:
        withdraw = await Withdraw.query.where(Withdraw.status == status).gino.first()
        return withdraw

    except:
        print("Не удалось найти заказ по статусу")


async def select_withdraw_by_id(id: int):
    withdraw = await Withdraw.query.where(Withdraw.id == id).gino.first()
    return withdraw


async def select_withdraw_by_user_id(user_id: int):
    try:
        withdraw = await Withdraw.query.where(Withdraw.user_id == user_id).gino.first()
        return withdraw

    except:
        print("Не удалось найти пользователя по его айди")


async def accept_withdraw(id: int, status: str = 'accepted'):
    withdraw = await Withdraw.query.where(Withdraw.id == id).gino.first()
    if withdraw:
        try:
            await withdraw.update(status=status).apply()
            return True
        except Exception as err:
            logging.exception(err)
    else:
        return False
    

async def select_photo_name_from_db(id: int):
    user = await Withdraw.query.where(Withdraw.id==id).gino.first()
    if user:
        try:
            photo_name = user.photo_name
            print(photo_name)
            return photo_name
        except Exception as err:
            print(err)
            print("ОШИБКА СБОРА ФОТО")
    else:
        print("Нет такого заказа")


async def select_photo_id_from_db(id: int):
    user = await Withdraw.query.where(Withdraw.id==id).gino.first()
    if user:
        try:
            photo_id = user.photo_id
            print(photo_id)
            return photo_id
        except Exception as err:
            print(err)
            print("ОШИБКА СБОРА ФОТО")
    else:
        print("Нет такого заказа")
