from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
import os
from data import config
from loader import dp
from utils.db_api import screen_commands, quick_commands as commands, google


@dp.callback_query_handler(Text('Скрины торговой площадки'), chat_id=config.admins, state=['*'])
async def get_screen(call: CallbackQuery):
    screen = await screen_commands.select_screen()
    if screen:
        user = await commands.select_user(screen.user_id)
        screen_name = await screen_commands.select_screen_name_from_db(screen.id)
        screen_id = await screen_commands.select_screen_id_from_db(screen.id)
        print(screen_name + "\n" + screen_id)
        try:
            await google.transver_from_withdraw_disc(screen_name, screen_id)
            print("Данный приняты")
        except:
            print("Ошибка принятия данных")
        try:
            screen_photo = open("D:/PYTHON/PROTECT_AIOGRAM/" + screen_name, "rb")
        except:
            print("Ошибка открытия файла")
        markup = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Подтвердить просмотр',
                                                                   callback_data=f'accept_screen{screen.id}')
                                          ],
                                          [
                                              InlineKeyboardButton(text='Отменить',
                                                                   callback_data='cancel_withdraw')
                                          ]
                                      ])
        await dp.bot.send_photo(chat_id=call.message.chat.id, photo=screen_photo)
        await call.message.answer(f'Пользователь (@{user.username} : {screen.user_id}) отправил скрин №{screen.id}\n'
                             f'Что будем делать',
                             reply_markup=markup)
        path = 'D:/PYTHON/PROTECT_AIOGRAM/' + screen_name
        try:
            os.remove(path)
        except:
            pass
    else:
        await call.message.answer(f'Сейчас нету скринов')


@dp.callback_query_handler(Text(startswith='accept_screen'), chat_id=config.admins)
async def accept_screen(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    try:
        screen_id = int(call.data.split('accept_screen')[1])
        screen = await screen_commands.select_screen_by_id(screen_id)
        if screen:
            if screen.status == 'created':
                if await screen_commands.accept_screen(screen_id):
                    try:
                        await dp.bot.send_message(screen.user_id, text=f'Ваш скрин под номером №{screen.id} был просмотрен одним из администраторов.')
                        await state.reset_state()
                    except Exception:
                        pass
                    finally:
                        await call.message.edit_text(f'Скрин под номером №{screen.id} был успешно просмотрен')
                        await asyncio.sleep(20)
                        await call.message.delete()
                else:
                    await screen_commands.accept_screen(screen.id, 'error')
                    await call.message.edit_text(f'Не удалось подтвердить осмотр скрина')
            else:
                await call.message.answer(f'Этот скрин уже был просмотрен другим администратором')
        else:
            await call.message.edit_text(f'Скрина с этим айди нету')
    except Exception:
        await call.message.edit_text('Неверный номер скрина')