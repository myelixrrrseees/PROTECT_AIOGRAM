from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from data import config
from loader import dp
from utils.db_api import withdraw_commands, quick_commands as commands, google


@dp.callback_query_handler(Text('Заявки оплаты'), chat_id=config.admins, state=['*'])
async def get_withdraw(call: CallbackQuery, state: FSMContext):
    withdraw = await withdraw_commands.select_withdraw()
    if withdraw:
        withdraw_id, user_id, amount, photo_name, photo_id, status = withdraw
        pre = amount * 0.67
        gold = float(f"{pre:.2f}")
        await state.update_data(gold=gold)
        user = await commands.select_user(user_id)
        await google.transver_from_withdraw_disc(photo_name, photo_id)
        photo = open("D:/PYTHON/PROTECT_AIOGRAM/" + photo_name, "rb")
        markup = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Подтвердить выплату',
                                                                   callback_data=f'accept_withdraw{withdraw_id}')
                                          ],
                                          [
                                              InlineKeyboardButton(text='Отклонить выплату',
                                                                   callback_data=f'close_withdraw{withdraw_id}')
                                          ],
                                          [
                                              InlineKeyboardButton(text='Отменить',
                                                                   callback_data='cancel_withdraw')
                                          ]
                                      ])

        await dp.bot.send_photo(chat_id=call.message.chat.id, photo=photo)
        # photo_message_id = photo_message.message_id
        # print(photo_message_id)
        await call.message.answer(f'Пользователь (@{user[3]} : {withdraw[1]}) создал заявку на выплату №{withdraw[0]}\n'
                                  f'Сумма выплаты: {withdraw[2]} - {gold} голды\n'
                                  f'Что будем делать',
                                  reply_markup=markup)
        path = 'D:/PYTHON/PROTECT_AIOGRAM/' + photo_name
        try:
            os.remove(path)
        except:
            pass
        # await state.update_data(photo_message=photo_message)
        # await dp.bot.delete_message(chat_id=photo_message.chat.id, message_id=photo_message.message_id)
    else:
        await call.message.answer(f'Сейчас нету активных заявок на выплату')
    

@dp.callback_query_handler(Text(startswith=f'accept_withdraw'), chat_id=config.admins)
async def accept_withdraw(call: CallbackQuery, state: FSMContext):
    try:
        await state.reset_state()
        get_id = int(call.data.split('accept_withdraw')[1])
        withdraw = await withdraw_commands.select_withdraw_by_id(get_id)
        withdraw_id, withdraw_user_id, amount, photo_name, photo_id, status = withdraw
        user = await commands.select_user(withdraw_user_id)
        user_user_id, first_name, last_name, username, attempts, referral_id = user
        ikb_screen = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text="Присласть скриншот оружия",
                                                                       callback_data=f'screen{withdraw_id}'),
                                              ],
                                          ])
        if withdraw:
            if status == 'created':
                if await withdraw_commands.accept_withdraw(withdraw_id):
                    try:
                        attempt = await commands.select_attempt(user_user_id)
                        number = attempt
                        number += 1
                        await commands.change_attempts(user_user_id, number)
                    except Exception as err:
                        print("Не удалось прибавить пользователю право на отправку скрина.")
                        print(err)
                    try:
                        await dp.bot.send_message(withdraw_user_id, text=f'Ваша заявка на оплату №{withdraw_id} была nодобрена '
                                                                         'Администратором 🧑‍💻\n'
                                                                         f'Пожалуйста, пришлите скриншот\n'
                                                                         "с выставленным оружием", reply_markup=ikb_screen)
                    except Exception as err:
                        print("Не удалось отправить пользователю")
                        print(err)
                    finally:
                        await call.message.edit_text(f'Заявка на оплату №{withdraw_id} была успешно одобрена')
                else:
                    await withdraw_commands.accept_withdraw(withdraw_id, 'error')
                    await call.message.edit_text(f'Не удалось подтвердить эту заявку на оплату')
            else:
                await call.message.edit_text(f'Эта заявка уже была обработана.')
        else:
            await call.message.edit_text(f'Заявки на оплату с этим айди нету')
    except Exception:
        await call.message.edit_text('Неверный номер заявки на оплату')


@dp.callback_query_handler(Text(startswith='close_withdraw'), chat_id=config.admins)
async def accept_withdraw(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    try:
        get_id = int(call.data.split('close_withdraw')[1])
        withdraw = await withdraw_commands.select_withdraw_by_id(get_id)

        withdraw_id, withdraw_user_id, amount, photo_name, photo_id, status = withdraw

        if withdraw:
            if status == 'created':
                if await withdraw_commands.accept_withdraw(withdraw_id, 'rejected'):
                    try:
                       await dp.bot.send_message(withdraw_user_id, text=f'Ваша заявка на оплату №{withdraw[0]} была отклонена')
                    except Exception:
                        pass
                    finally:
                        await call.message.edit_text(f'Заявка на оплату №{withdraw[0]} была успешно отклонена')
                else:
                    await withdraw_commands.accept_withdraw(withdraw[0], 'error')
                    await call.message.edit_text(f'Не удалось отклонить эту заявку на оплату')
            else:
                await call.message.answer(f'Эта заявка уже была обработана.')
        else:
            await call.message.edit_text(f'Заявки на оплату с этим айди нету')
    except Exception:
        await call.message.edit_text("Неверный номер заявки на оплату")
