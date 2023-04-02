from filters import IsPrivate
from states import calculator as cal
from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

to_pay_btn = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Перейти к оплате', callback_data='next_gold')
                                      ]
                                  ])


@dp.message_handler(IsPrivate(), text='🧮 Калькулятор')
async def calculator(message: types.Message, state: FSMContext):
    await state.reset_state()
    msg = await message.answer('Напишите число в рублях (без копеек):')
    await state.update_data(message_ids=msg.message_id)
    await cal.num.set()


@dp.callback_query_handler(text='calculator')
async def calculator(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state()
    msg = await call.message.answer('Напишите число в рублях (без копеек):')
    await state.update_data(message_ids=msg.message_id)
    await cal.num.set()


@dp.message_handler(IsPrivate(), state=cal.num)
async def total_number(message: types.Message, state: FSMContext):
    chislo = float(message.text)
    total = chislo * 0.67
    await state.reset_state()
    await message.answer(f"{chislo} рублей - {total} золота.", reply_markup=to_pay_btn)
