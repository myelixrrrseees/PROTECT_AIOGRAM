from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💰 Покупка золота'),
            KeyboardButton(text='🧮 Калькулятор')
        ],
        [
            KeyboardButton(text='🆕 Другие товары'),
            KeyboardButton(text='📢 Отзывы'),
            KeyboardButton(text='🛠 Тех поддержка')
        ]
    ],
    resize_keyboard=True
)
