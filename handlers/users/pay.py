import asyncio
import logging
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentType

from filters import IsPrivate, IsDatabaseUser
from loader import dp
from states import withdraw
from utils.db_api import withdraw_commands, quick_commands as commands, google
from data.config import folder
from keyboards.inline_kbs import ikb_withdraw

cancel_btn = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Отменить',
                                                               callback_data='cancel_withdraw')
                                      ]
                                  ])


bank_btns = InlineKeyboardMarkup(row_width=1,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='Тинькофф', callback_data='tinkoff')
                                     ],
                                     [
                                         InlineKeyboardButton(text='Сбербанк', callback_data='sber')
                                     ],
                                     [
                                         InlineKeyboardButton(text='Киви', callback_data='qiwi')
                                     ],
                                     [
                                         InlineKeyboardButton(text='Отменить', callback_data='cancel_withdraw')
                                     ]
                                 ])


@dp.message_handler(Text('💰 Голда'))
async def create_withdraw(message: Message, state: FSMContext):
    await state.reset_state()
    msg = await message.answer('Введите сумму выплаты (минимум 50):',
                                    reply_markup=cancel_btn)
    await state.update_data(message_ids=msg.message_id)
    await withdraw.amount.set()


@dp.message_handler(IsPrivate(), IsDatabaseUser(), state=withdraw.amount)
async def get_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        pre = amount * 0.67
        cal = float(f"{pre:.2f}")
        if amount >= 50:
            await state.update_data(withdraw_amount=amount)
            msg_gold = await message.answer(f'{amount} рублей - {cal} голды\n'
                                    f'Теперь выберете банк',
                                    reply_markup=bank_btns)
            await state.update_data(msg_gold=msg_gold)
        else:
            msg = await message.reply(f'Минимальная сумма для выплаты 50 рублей',
                                        reply_markup=cancel_btn)
            await asyncio.sleep(20)
            await message.delete()
            await msg.delete()
    except ValueError:
        msg = await message.reply(f'Введите сумму выплаты числом (пример: 180.5).',
                                  reply_markup=cancel_btn)
        await asyncio.sleep(20)
        await message.delete()
        await msg.delete()
    except Exception:
        msg = await message.answer(f'Неизвестная ошибка.\n\n'
                                   f'Введите сумму выплаты числомю',
                                   reply_markup=cancel_btn)
        await asyncio.sleep(20)
        await message.delete()
        await msg.delete()


@dp.callback_query_handler(Text('tinkoff'), state=['*'])
async def tinkoff_pay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = await call.message.answer('Наши реквизиты\n'
                                    f'Сумма: {data.get("withdraw_amount")}\n'
                                    '...............\n'
                                    '...............\n'
                                    '\n'
                                    'Как только переведете, отправте скрин чека')
    await withdraw.photo.set()
    await state.update_data(msg=msg)


@dp.callback_query_handler(Text('sber'), state=['*'])
async def sber_pay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = await call.message.answer('Наши реквизиты\n'
                              f'Сумма: {data.get("withdraw_amount")}\n'
                              '...............\n'
                              '...............\n'
                              '\n'
                              'Как только переведете, отправте скрин чека')
    await withdraw.photo.set()
    await state.update_data(msg=msg)
    

@dp.callback_query_handler(Text('qiwi'), state=['*'])
async def qiwi_pay(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = await call.message.answer('Наши реквизиты\n'
                              f'Сумма: {data.get("withdraw_amount")}\n'
                              '...............\n'
                              '...............\n'
                              '\n'
                              'Как только переведете, отправте скрин чека')
    await withdraw.photo.set()
    await state.update_data(msg=msg)


@dp.message_handler(IsPrivate(), IsDatabaseUser(), state=withdraw.photo, content_types=ContentType.PHOTO)
async def get_address(message: Message, state: FSMContext):

    photo_id = message.photo[-1].file_id
    photo = await dp.bot.get_file(photo_id)
    print(photo)
    filename = photo.file_path
    destination = r"D:/PYTHON/PROTECT_AIOGRAM/" + filename
    await dp.bot.download_file(filename, destination)

    try:
        photo_id = await google.transver_withdraw(filename)
        await state.update_data(withdraw_photo_name=filename)
        await state.update_data(withdraw_photo_id=photo_id)
        data = await state.get_data()
        withdraw_id = await withdraw_commands.create_withdraw(user_id=message.from_user.id,
                                                              amount=float(data.get("withdraw_amount")),
                                                              photo_name=str(data.get("withdraw_photo_name")),
                                                              photo_id=str(data.get("withdraw_photo_id")),
                                                              status='created')
        if withdraw_id:
            try:
                path = 'D:/PYTHON/PROTECT_AIOGRAM/' + filename
                try:
                    os.remove(path)
                except:
                    pass
                await message.answer('Заказ успешно создан ❗️\n'
                                     'Пожалуйста, ожидайте \nподтверждения оплаты.')
                await dp.bot.send_message(1194575524, text="Поступила новая заявка оплаты.\n\n"
                                  "Нажмите на кнопку ниже, чтобы посмотреть заявку", reply_markup=ikb_withdraw)
                
                
            except Exception as err:
                logging.exception(err)
                await message.answer('При создании заявки на оплату произошла ошибка.')
                try:
                    await withdraw_commands.accept_withdraw(id=withdraw_id,
                                                            status='error')
                except Exception:
                    pass
        else:
            await message.answer(f'Ваш баланс меньше суммы оплаты')
    except Exception:
        await message.answer('При создании заявки на оплату произошла ошибка')
    finally:
        await state.reset_state()
    # for message_id in str(data.get('message_ids')).split(', '):
    #     try:
    #         await dp.bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
    #         await asyncio.sleep(0.5)
    #     except Exception as err:
    #         print(err)
    # else:
    #     await message.delete()
    # await asyncio.sleep(0.5)
    # msg_data = data.get("msg")
    # msg_gold = data.get("msg_gold")
    # await msg_gold.delete()
    # await msg_data.delete()


@dp.callback_query_handler(Text('cancel_withdraw'), state=['*'])
async def cancel_withdraw(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.reset_state()
    await call.message.edit_text('Отменено')
    if data.get('message_ids'):
        for message_id in str(data.get('message_ids')).split(', '):
            try:
                await dp.bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
                await asyncio.sleep(0.5)
            except Exception as err:
                print(err)
                await asyncio.sleep(0.5)
