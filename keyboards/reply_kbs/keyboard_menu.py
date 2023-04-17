from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💰 Голда'),
            KeyboardButton(text='🧮 Калькулятор'),
            KeyboardButton(text='📢 Отзывы'),
        ],
        [
            KeyboardButton(text='‼️ Правила покупки'),
            KeyboardButton(text='🛠 Тех поддержка')
        ]
    ],
    resize_keyboard=True
)
