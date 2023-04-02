from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_withdraw = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Заявки оплаты', callback_data='Заявки оплаты'),
                                    ],
                                ]
)