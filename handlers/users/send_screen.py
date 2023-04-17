from aiogram.dispatcher import FSMContext
import logging
import asyncio
from aiogram.dispatcher.filters import Text
from filters import IsPrivate, IsDatabaseUser
from loader import dp
from states import send_screen
from aiogram import types
from utils.db_api import screen_commands, google, quick_commands as commands, withdraw_commands
from keyboards.inline_kbs import ikb_screen
from states import send_screen


@dp.callback_query_handler(Text(startswith=f"screen"))
async def _screen(call: types.CallbackQuery, state: FSMContext):
    get_id = int(call.data.split('screen')[1])
    withdraw = await withdraw_commands.select_withdraw_by_id(get_id)
    withdraw_id, withdraw_user_id, amount, photo_name, photo_id, status = withdraw

    pre = amount * 0.67
    gold = float(f"{pre:.2f}")
    await state.update_data(gold=gold)

    attempt = await commands.select_attempt(call.from_user.id)
    if attempt > 0:
        number = attempt
        number -= 1
        await call.message.answer(f'Пожалуйста, пришлите скриншот\n'
                                  "с выставленным оружием")
        await commands.change_attempts(call.from_user.id, number)
        await send_screen.screen.set()
    else:
        await call.message.answer("Вы не покупали голду.")


@dp.message_handler(IsPrivate(), IsDatabaseUser(), state=send_screen.screen, content_types=types.ContentType.PHOTO)
async def _send_screen(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    print(message.from_user.id)
    print("Фото дошло")
    photo = await dp.bot.get_file(photo_id)
    # print(photo)
    screen_name = photo.file_path
    destination = r"D:/PYTHON/PROTECT_AIOGRAM/" + screen_name
    await dp.bot.download_file(screen_name, destination)

    try:
        screen_id = await google.transver_screen_to_disk(screen_name)
        await state.update_data(screen_name=screen_name)
        await state.update_data(screen_id=screen_id)
        data = await state.get_data()
        print(float(data.get("gold")))
        screen_id = await screen_commands.create_screen(user_id=message.from_user.id,
                                                        gold=float(data.get("gold")),
                                                        screen_name=str(data.get("screen_name")),
                                                        screen_id=str(data.get('screen_id')),
                                                        status='created')
        if screen_id:
            try:
                await message.answer('Скрин успешно отправлен ❗️\n'
                                     'Пожалуйста, ожидайте ответа администратора.\n')
                await dp.bot.send_message(1194575524, text="Пришол новый скрин торговой площадки", reply_markup=ikb_screen)
            except Exception as err:
                logging.exception(err)
                await message.answer(' 1  При отправки скрина произошла ошибка.')
                try:
                    await screen_commands.accept_screen(screen_id, status='error')
                except Exception:
                    pass
        else:
            await message.answer(f'Это не фото')
    except Exception as err:
        await message.answer('  2  При отправки скрина произошла ошибка.')
        print(err)
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
