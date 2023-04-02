from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from data import config
from loader import dp
from utils.db_api import withdraw_commands, quick_commands as commands, google
from states import send_screen


@dp.callback_query_handler(Text('Заявки оплаты'), chat_id=config.admins, state=['*'])
async def get_withdraw(call: CallbackQuery, state: FSMContext):
    withdraw = await withdraw_commands.select_withdraw()
    if withdraw:
        print("ДАнные из базы\n\n"
              f"Номер заказа: {withdraw.id}")
        user = await commands.select_user(withdraw.user_id)
        photo_name = await withdraw_commands.select_photo_name_from_db(withdraw.id)
        photo_id = await withdraw_commands.select_photo_id_from_db(withdraw.id)
        print(photo_name + "\n" + photo_id)
        try:
            await google.transver_from_withdraw_disc(photo_name, photo_id)
            print("Данный приняты")
        except:
            print("Ошибка принятия данных")
        try:
            photo = open("D:/PYTHON/PROTECT_AIOGRAM/" + photo_name, "rb")
        except:
            print("Ошибка открытия файла")
        markup = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Подтвердить выплату',
                                                                   callback_data=f'accept_withdraw{withdraw.id}')
                                          ],
                                          [
                                              InlineKeyboardButton(text='Отклонить выплату',
                                                                   callback_data=f'close_withdraw{withdraw.id}')
                                          ],
                                          [
                                              InlineKeyboardButton(text='Отменить',
                                                                   callback_data='cancel_withdraw')
                                          ]
                                      ])
        await dp.bot.send_photo(chat_id=call.message.chat.id, photo=photo)
        await call.message.answer(f'Пользователь (@{user.username} : {withdraw.user_id}) создал заявку на выплату №{withdraw.id}\n'
                             f'Сумма выплаты: {withdraw.amount}\n'
                             f'Что будем делать',
                             reply_markup=markup)
        path = 'D:/PYTHON/PROTECT_AIOGRAM/' + photo_name
        try:
            os.remove(path)
        except:
            pass
    else:
        await call.message.answer(f'Сейчас нету активных заявок на выплату')
    


@dp.callback_query_handler(Text(startswith='accept_withdraw'), chat_id=config.admins)
async def accept_withdraw(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    try:
        withdraw_id = int(call.data.split('accept_withdraw')[1])
        withdraw = await withdraw_commands.select_withdraw_by_id(withdraw_id)
        print(withdraw.user_id)
        if withdraw:
            if withdraw.status == 'created':
                if await withdraw_commands.accept_withdraw(withdraw_id):
                    try:
                        await dp.bot.send_message(withdraw.user_id, text=f'Ваша заявка на выплату №{withdraw.id} была одобрена одним администраторов.\n'
                                                                         f'Пожалуйста, скиньте скрин из торговой площадки')
                        await send_screen.screen.set()
                    except Exception as err:
                        print("Не удалось отправить пользователю")
                        print(err)
                    finally:
                        await call.message.edit_text(f'Заявка на выплату №{withdraw.id} была успешно одобрена')
                else:
                    await withdraw_commands.accept_withdraw(withdraw.id, 'error')
                    await call.message.edit_text(f'Не удалось подтвердить эту заявку на выплату')
            else:
                await call.message.edit_text(f'Эта заявка на выплату уже обработана другим администратором')
        else:
            await call.message.edit_text(f'Заявки на выплату с этим айди нету')
    except Exception:
        await call.message.edit_text('Неверный номер заявки на выплату')
    data = await state.get_data()
    for message_id in str(data.get('message_ids')).split(', '):
        try:
            await dp.bot.delete_message(chat_id=call.message.from_user.id, message_id=message_id)
            await asyncio.sleep(0.5)
        except Exception as err:
            print(err)
    else:
        await call.message.delete()

@dp.callback_query_handler(Text(startswith='close_withdraw'), chat_id=config.admins)
async def accept_withdraw(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    try:
        withdraw_id = int(call.data.split('close_withdraw')[1])
        withdraw = await withdraw_commands.select_withdraw_by_id(withdraw_id)
        if withdraw:
            if withdraw.status == 'created':
                if await withdraw_commands.accept_withdraw(withdraw_id, 'rejected'):
                    try:
                       await dp.bot.send_message(withdraw.user_id, text=f'Ваша заявка на выплату №{withdraw.id} была отклонена')
                    except Exception:
                        pass
                    finally:
                        await commands.change_balance(withdraw.user_id, withdraw.amount)
                        await call.message.edit_text(f'Заявка на выплату №{withdraw.id} была успешно отклонена')
                else:
                    await withdraw_commands.accept_withdraw(withdraw.id, 'error')
                    await call.message.edit_text(f'Не удалось отклонить эту заявку на выплату')
            else:
                await call.message.answer(f'Эта заявка на выплату уже обработана другим администратором')
        else:
            await call.message.edit_text(f'Заявки на выплату с этим айди нету')
    except Exception:
        await call.message.edit_text("Неверный номер заявки на выплату")
    data = await state.get_data()

    for message_id in str(data.get('message_ids')).split(', '):
        try:
            await dp.bot.delete_message(chat_id=call.message.from_user.id, message_id=message_id)
            await asyncio.sleep(0.5)
        except Exception as err:
            print(err)
    else:
        await call.message.delete()