from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_screen = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Скрины торговой площадки', callback_data='Скрины торговой площадки'),
                                    ],
                                  ]
)