import telebot

bot = telebot.TeleBot('6871845196:AAGooDGNQw0FdAH8sf7rSSU8UmAZLcKH3IY')

QUEST = {1:['', {'start':21}],
         21:['123', 'WIN']}
history = 1
start = False

@bot.message_handler(content_types=['text'])
def send_text(chat):
    global start
    global history
    print(chat)
    history = QUEST[history][1][chat.text]
    if QUEST[history][1] == 'LOSE':
        bot.send_message(chat.chat.id, str(QUEST[history][0]))
    elif QUEST[history][1] == 'WIN':
        bot.send_message(chat.chat.id, str(QUEST[history][0]))
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        for i in QUEST[history][1].keys():
            keyboard.add(telebot.types.InlineKeyboardButton(text=i))
        bot.send_message(chat.chat.id, str(QUEST[history][0]), reply_markup=keyboard)

bot.polling()