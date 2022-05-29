#Реализовано для Saber Interactive на вакансию QA Automation Engineer Junior

import logging
from aiogram import Bot, Dispatcher, executor, types
from db import Database

BOT_TOKEN = "Token"

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


GIVE_KEY = "Введите пароль:"
KEY = "SaberInteractive"
START_MESSAGE = '''Привет! Введи математическое выражение с доступными ниже операторами.

***Операторы***:
+ - сложение;
- - вычитание;
* - умножение;
/ - деление;
** - возведение в степнь.

***Например***: 
2+1 
9*9 
2*6/8 
20-2*10
100**100'''


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        await bot.send_message(message.chat.id, GIVE_KEY)
    else:
        await bot.send_message(message.from_user.id, START_MESSAGE)


# Обработчик сообщений
@dp.message_handler()
async def get_text_messages(message: types.Message):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.id):
            if message.text == KEY:
                db.add_user(message.from_user.id)
                await bot.send_message(message.from_user.id, START_MESSAGE)
            else:
                await bot.send_message(message.chat.id, GIVE_KEY)
        else:
            try:
                await bot.send_message(message.chat.id, eval(message.text))
            except (SyntaxError, NameError, TypeError):
                await bot.send_message(message.chat.id, "Похоже, что в выражении есть ошибка")
            except ZeroDivisionError:
                await bot.send_message(message.chat.id, "На ноль делить нельзя :)")




# Вход в программу
if (__name__ == '__main__'):
    executor.start_polling(dp, skip_updates= True)
