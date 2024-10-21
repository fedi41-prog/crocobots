import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('6871845196:AAGooDGNQw0FdAH8sf7rSSU8UmAZLcKH3IY')

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('croco_data_base.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Ригистрация! Введи твоё имя или СЪЕМ!')
    bot.register_next_step_handler(message, user_name)
def user_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, 'А теперь пароль.')
    bot.register_next_step_handler(message, user_pass)
    


bot.polling()
