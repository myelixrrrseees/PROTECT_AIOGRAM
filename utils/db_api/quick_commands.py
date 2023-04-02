from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemes.user import User


async def add_user(user_id: int, first_name: str, last_name: str, username: str):

    try:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username)
        await user.create()
        print("Пользователь добавлен в базу данных")
        return user

    except UniqueViolationError:
        print('Пользователь не добавлен')


async def select_all_users():
    try:
        users = await User.query.gino.all()
        return users
    except:
        print("Не удалось ")


async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user(user_id: int):
    try:
        user = await User.query.where(User.user_id == user_id).gino.first()
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


