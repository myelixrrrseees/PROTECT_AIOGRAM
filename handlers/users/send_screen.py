from aiogram.dispatcher import FSMContext
import logging
import asyncio
from loader import dp
from states import send_screen
from aiogram import types
from utils.db_api import screen_commands, google
from keyboards.inline_kbs import ikb_screen


@dp.message_handler(state=send_screen.screen, content_types=types.ContentType.PHOTO)
async def screen(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    print("Фото дошло")
    print(photo_id)
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
        screen_id = await screen_commands.create_screen(user_id=message.from_user.id,
                                                        screen_name=str(data.get("screen_name")),
                                                        screen_id=str(data.get('screen_id')),
                                                        status='created')
        if screen_id:
            try:
                await message.answer('Скрин успешно отправлен!\n'
                                    'Пожалуйста, ожидайте ответа администратора.\n')
                await dp.bot.send_message(1194575524, text="Пришол новый скрин торговой площадки", reply_markup=ikb_screen)
            except Exception as err:
                logging.exception(err)
                await message.answer('При отправки скрина произошла ошибка.')
                try:
                    await screen_commands.accept_screen(id=screen_id,
                                                            status='error')
                except Exception:
                    pass
        else:
            await message.answer(f'Это не фото')
    except Exception:
        await message.answer('При отправки скрина произошла ошибка.')
    finally:
        await state.reset_state()
    for message_id in str(data.get('message_ids')).split(', '):
        try:
            await dp.bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
            await asyncio.sleep(0.5)
        except Exception as err:
            print(err)
    else:
        await message.delete()
