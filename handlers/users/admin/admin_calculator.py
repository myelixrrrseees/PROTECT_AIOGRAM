from data.config import admins
from states import calculator as cal
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types


@dp.callback_query_handler(text='Курс золота', chat_id=admins, state=['*'])
async def calculator(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    msg = await call.message.answer('Напишите число в рублях (без копеек)')
    await state.update_data(message_ids=msg.message_id)
    await cal.num.set()


@dp.message_handler(state=cal.num, chat_id=admins)
async def total_number(message: types.Message, state: FSMContext):
    chislo = float(message.text)
    total = chislo * 0.67

    await message.answer(f"{chislo} рублей - {total} золота")
    await state.reset_state()