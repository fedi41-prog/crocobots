import telebot
from telebot import types

bot = telebot.TeleBot('6871845196:AAGooDGNQw0FdAH8sf7rSSU8UmAZLcKH3IY')


@bot.message_handler(commands=['start'])
def crocodile_hello(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} я крокобот 🐊🤖.')
    bot.register_next_step_handler(message, reply_to_hello)
@bot.message_handler(content_types=['photo'])
def reply_to_photo(message):
    bot.reply_to(message, 'вкусняшка!')
def reply_to_hello(message):
    hello = ['привет',
             'приветик',
             'здравствуй',
             'здравствуйте',
             'приветствую',
             'добрый день',
             'доброе утро',
             'добрый вечер']
    for i in hello:
        if i in message.text.lower():
            bot.send_message(message.chat.id, 'И тебе приветик! вкусный человечек [:')
            break
bot.polling()