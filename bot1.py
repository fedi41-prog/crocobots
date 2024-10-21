import telebot, datetime

bot = telebot.TeleBot('6855325883:AAGhy45KiCIW5-KrqjxTPN5Nk0m6CM3Bg4E')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('/start', 'привет', 'пока', 'дата', 'время', 'день недели')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет ты написал мне /start', reply_markup=keyboard1)
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() in ['привет', 'пока']:
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id, 'И тебе привет!', reply_markup=keyboard1)
        elif message.text.lower() == 'пока':
            bot.send_message(message.chat.id, 'И тебе пока!', reply_markup=keyboard1)
    elif message.text.lower() in ['дата', 'время', 'день недели']:
        weekdays = ['понедельник',
                    'вторник',
                    'среда',
                    'четверг',
                    'пятница',
                    'суббота',
                    'воскресение']
        day = datetime.datetime.today()
        time = datetime.datetime.now()
        if message.text.lower() == 'дата':
            bot.send_message(message.chat.id, day.date(), reply_markup=keyboard1)
        elif message.text.lower() == 'время':
            bot.send_message(message.chat.id, time.time(), reply_markup=keyboard1)
        elif message.text.lower() == 'день недели':
            bot.send_message(message.chat.id, weekdays[day.weekday()],
                             reply_markup=keyboard1)
bot.polling()