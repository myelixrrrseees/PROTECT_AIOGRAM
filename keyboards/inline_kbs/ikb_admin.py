from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_admin = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Заявки оплаты', callback_data='Заявки оплаты'),
                                    ],
                                    [
                                        InlineKeyboardButton(text='Скрины торговой площадки', callback_data='Скрины торговой площадки'),
                                    ],
                                    [
                                        InlineKeyboardButton(text='Рассылка', callback_data='Рассылка'),
                                    ],
                                    [
                                        InlineKeyboardButton(text='Канал отзывов', callback_data='Канал отзывов'),
                                    ],
                                    [
                                        InlineKeyboardButton(text='Курс золота', callback_data='gold_rate')
                                    ]
                                ])
