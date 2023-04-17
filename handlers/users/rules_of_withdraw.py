from loader import dp
from aiogram import types


@dp.message_handler(text="‼️ Правила покупки")
async def rules_of_withdraw(message: types.Message):
    await message.answer('1️⃣ Нажимаем на кнопу "Покупка голды".'
                         '\nНеобходимо написать, на сколько рублей вы хотите произвести покупку (не менее 50 рублей)\n\n'
                         '2️⃣ Выбираете банк (Тут, думаю, вы справитесь)\n'
                         'Бот пришлет вам реквизиты. Как только вы переведете сумму на указанный номер телефона,\n'
                         'сделайте скрин успешного перевода.\n'
                         'Дальше остается ждать ответа администратора.\n\n'
                         '3️⃣ Как только вам придет оповещение от бота о подтверждении оплаты администратором,\n'
                         'необходимо будет скинуть скрин выставленного оружия на торговой площадки \n(цена должна быть такой'
                         'же, сколько вы купили)\n\n'
                         '4️⃣ Как только вам придет оповещение от бота, что скрин был просмотрен,\n'
                         'вы можете зайти в игру и проверить баланс.\n\n'
                         '🛠 Если у вас возникнут вопросы, нажмите на кнопу "Тех поддержка".\n\n'
                         'Приятной покупки 😉')