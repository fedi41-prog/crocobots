import telebot
from telebot import types
import json
import random
import cv2

bot = telebot.TeleBot('6871845196:AAGooDGNQw0FdAH8sf7rSSU8UmAZLcKH3IY')

with open('user_status.json', 'rb') as data:
    user_status = json.load(data)
with open('settings.json', 'rb') as data:
    settings = json.load(data)
with open('tests.json', 'rb') as data:
    tests = json.load(data)
    tests_list = ''
    for test_nr in tests.keys():
        test_name = tests[test_nr]['name']
        tests_list += f'{test_nr} - {test_name}'

def save_user_status():
    with open('user_status.json', 'w') as data:
        json.dump(user_status, data)
def save_settings():
    with open('settings.json', 'w') as data:
        json.dump(settings, data)

class Functions:
    @staticmethod
    def jumpscare():
        while True:
            img = cv2.imread('R.png')
            cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("window", img)
            key = cv2.waitKey(0)
            if key == 27:
                break

class Games:
    @staticmethod
    def sticks(message):
        username = message.from_user.username
        def calculate(sticks_left, sticks_max, level):
            sticks_level = round(sticks_left / 100 * level)
            if sticks_level <= sticks_level:
                res = (sticks_left - 1) % (sticks_max + 1)
                if not res:
                    return res
            return random.randint(1, sticks_max)
        if user_status[username]['running'] == 'games>play>sticks':
            user_status[username]['running'] = 'games>play>sticks>settings>sticks_given'
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Введите ')



@bot.message_handler(commands=['start', 'tests', 'games', 'admin'])
def check_commands(message):
    games = ['sticks']
    try:
        username = message.from_user.username
        if message.text == '/start':
            markup = types.ReplyKeyboardMarkup()
            markup.add('/start')
            markup.add('/tests')
            markup.add('/games')
            user_status[username] = {'running':'start'}
            #,
            bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} я Крокобот 🐊🤖.')
            bot.send_message(message.chat.id, '''Вот несколько команд для управления:
            /start - перезапустить Крокобота,
            /tests - проходить тесты.
            /games - играть в игры
            ''', reply_markup=markup)

        elif message.text == '/tests':
            markup = types.ReplyKeyboardMarkup()
            for i in tests.keys():
                markup.add(tests[i]['name'])
            user_status[username]['running'] = 'tests>choice'
            bot.send_message(message.chat.id, 'Вот все тесты которые можно пройти!', reply_markup=markup)
            bot.send_message(message.chat.id, tests_list)
            bot.send_message(message.chat.id, 'Введите номер или название теста.')
        elif message.text == '/games':
            markup = types.ReplyKeyboardMarkup()
            for i in games:
                markup.add(i)
            user_status[username]['running'] = 'games>choice_game'
            bot.send_message(message.chat.id, 'Выберите игру.', reply_markup=markup)
        elif message.text == '/admin':
            if user_status[username]['running'].startswith('admin'):
                user_status[username]['running'] = 'admin>restart'
                admin(message)
            else:
                end_markup = types.ReplyKeyboardRemove()
                user_status[username]['running'] = 'admin>enter_passwort'
                bot.send_message(message.chat.id, 'Введите код админисратора чтобы продолжить.', reply_markup=end_markup)
        save_user_status()
        save_settings()
    except Exception:
        end_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, '❌❌❌>ERROR<❌❌❌', reply_markup=end_markup)

@bot.message_handler(content_types=['text'])
def check_text(message):
    try:
        username = message.from_user.username
        if user_status[username]['running'].split('>')[0] == 'tests':
            test(message)
        elif user_status[username]['running'].split('>')[0] == 'start':
            easy_chat(message)
        elif user_status[username]['running'].split('>')[0] == 'games':
            games(message)
        elif user_status[username]['running'].split('>')[0] == 'admin':
            admin(message)

        save_user_status()
        save_settings()

    except Exception:
        end_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, '❌❌❌>ERROR<❌❌❌', reply_markup=end_markup)

def games(message):
    games_names = {'sticks':'sticks'}
    games = {'sticks':Games.sticks}
    username = message.from_user.username
    if user_status[username]['running'] == 'games>choice_game':
        if message.text in games_names.keys():
            user_status[username]['running'] = 'games>play>'+games_names[message.text]
            games[games_names[message.text]](message)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста выберайте из вариантов!')
    elif user_status[username]['running'].startswith('games>play>'):
        games[games_names[user_status[username]['running'].split('>')[2]]](message)

def easy_chat(message):
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

def test(message):

    username = message.from_user.username
    if user_status[username]['running'] == 'tests>choice':
        for i in tests.keys():
            if message.text == i or message.text == tests[i]['name']:
                markup = types.ReplyKeyboardRemove()
                user_status[username] = {'running':'tests>play', 'tests': {'results': {}, 'current_question': 0, 'test_nr': i}}
                for i2 in tests[i]['results'].keys():
                    user_status[username]['tests']['results'][i2] = 0
                bot.send_message(message.chat.id, 'Ок начнём!', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Пожалуйста выберайте из вариантов!')
    elif user_status[username]['running'].split('>')[1] == 'play':
        test_nr = user_status[username]['tests']['test_nr']
        question_nr = user_status[username]['tests']['current_question']
        if message.text in tests[test_nr]['questions'][question_nr]['answers'].keys():
            for i in tests[test_nr]['questions'][question_nr]['answers'][message.text]:
                if i.count('+') == 1:
                    user_status[username]['tests']['results'][i.split('+')[0]] += int(i.split('+')[1])
                elif i.count('-') == 1:
                    user_status[username]['tests']['results'][i.split('-')[0]] -= int(i.split('-')[1])
            user_status[username]['tests']['current_question'] = question_nr + 1
            if not len(tests[test_nr]['questions']) > question_nr+1:
                user_status[username]['running'] = 'tests>end'
                end_markup = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, 'Ок, тест пройден!', reply_markup=end_markup)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста выберайте из вариантов!')
    if user_status[username]['running'] != 'tests>end' and user_status[username]['running'] != 'tests>choice':
        test_nr = user_status[username]['tests']['test_nr']
        question_nr = user_status[username]['tests']['current_question']
        markup = types.ReplyKeyboardMarkup()
        for answer in tests[test_nr]['questions'][question_nr]['answers'].keys():
            markup.add(answer)
        bot.send_message(message.chat.id, tests[test_nr]['questions'][question_nr]['question'],
                             reply_markup=markup)
    elif user_status[username]['running'] != 'tests>choice':
        test_nr = user_status[username]['tests']['test_nr']
        results_dict = user_status[username]['tests']['results']
        best_results = []
        for result_key in results_dict.keys():
            if best_results == []:
                best_results.append(result_key)
            elif results_dict[result_key] > results_dict[best_results[0]]:
                best_results = [result_key]
            elif results_dict[result_key] == results_dict[best_results[0]]:
                best_results.append(result_key)
        bot.send_message(message.chat.id, tests[test_nr]['results'][random.choice(best_results)])
        user_status[username] = {'running':'start', 'tests':{'results':{}, 'current_question':None, 'test_nr':None}}
    save_user_status()

def admin(message):
    activities_names = {'Запустить функцию':'start_func', 'Поменять пароль':'change_passwort'}
    activities = {'start_func':start_code, 'change_passwort':change_passwort}

    admin_passwort = settings['admin']['passwort']

    username = message.from_user.username
    if user_status[username]['running'] == 'admin>enter_passwort':
        if message.text == admin_passwort:
            markup = types.ReplyKeyboardMarkup()
            end_markup = types.ReplyKeyboardRemove()
            user_status[username]['running'] = 'admin>chose_activity'
            for i in activities_names.keys():
                markup.add(i)
            bot.send_message(message.chat.id, 'Пароль правильный! Вход разрешён.', reply_markup=end_markup)
            bot.send_message(message.chat.id, 'Выбирите дейсвие:', reply_markup=markup)
        else:
            end_markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Пароль неправильный! Вход запрешён.', reply_markup=end_markup)
    elif user_status[username]['running'] == 'admin>chose_activity':
        if message.text in activities_names.keys():
            activities[activities_names[message.text]](message)
        else:
            markup = types.ReplyKeyboardMarkup()
            end_markup = types.ReplyKeyboardRemove()
            for i in activities_names.keys():
                markup.add(i)
            bot.send_message(message.chat.id, f'Нет действия "{message.text}"', reply_markup=end_markup)
            bot.send_message(message.chat.id, 'Выбирите дейсвие:', reply_markup=markup)
    elif user_status[username]['running'].startswith('admin>run_activity>'):
        activities[user_status[username]['running'].split('>')[2]](message)
    elif user_status[username]['running'] == 'admin>restart':
        markup = types.ReplyKeyboardMarkup()
        user_status[username]['running'] = 'admin>chose_activity'
        for i in activities_names.keys():
            markup.add(i)
        bot.send_message(message.chat.id, 'Выбирите дейсвие:', reply_markup=markup)

def start_code(message):
    functions = {'jumpscare':Functions.jumpscare}
    username = message.from_user.username
    if user_status[username]['running'] == 'admin>chose_activity':
        user_status[username]['running'] = 'admin>run_activity>start_func>chose_func'
        markup = types.ReplyKeyboardMarkup()
        for i in functions.keys():
            markup.add(i)
        bot.send_message(message.chat.id, 'Выбирите фунцию:', reply_markup=markup)
    elif user_status[username]['running'] == 'admin>run_activity>start_func>chose_func':
        if message.text in functions.keys():
            user_status[username]['running'] = 'admin>restart'
            end_markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Функция запусщена...', reply_markup=end_markup)
            functions[message.text]()
            bot.send_message(message.chat.id, 'Выпонение функции закончено!', reply_markup=end_markup)
            admin(message)
        else:
            end_markup = types.ReplyKeyboardRemove()
            markup = types.ReplyKeyboardMarkup()
            for i in functions.keys():
                markup.add(i)
            bot.send_message(message.chat.id, f'Нет функции "{message.text}"', reply_markup=end_markup)
            bot.send_message(message.chat.id, 'Выбирите фунцию:', reply_markup=markup)
def change_passwort(message):
    username = message.from_user.username
    if user_status[username]['running'] == 'admin>chose_activity':
        user_status[username]['running'] = 'admin>run_activity>change_passwort>enter_old_passwort'
        end_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите старый пароль чтобы установить новый.', reply_markup=end_markup)
    elif user_status[username]['running'] == 'admin>run_activity>change_passwort>enter_old_passwort':
        if message.text == settings['admin']['passwort']:
            user_status[username]['running'] = 'admin>run_activity>change_passwort>enter_new_passwort'
            end_markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Пароль правильный!', reply_markup=end_markup)
            bot.send_message(message.chat.id, 'Введите новый пароль:', reply_markup=end_markup)
        else:
            user_status[username]['running'] = 'admin>restart'
            end_markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Пароль неравильный!', reply_markup=end_markup)
            bot.send_message(message.chat.id, 'Доступ запрещён.', reply_markup=end_markup)
            admin(message)
    elif user_status[username]['running'] == 'admin>run_activity>change_passwort>enter_new_passwort':
        user_status[username]['running'] = 'admin>restart'
        end_markup = types.ReplyKeyboardRemove()
        settings['admin']['passwort'] = message.text
        bot.send_message(message.chat.id, 'Пароль успешно изменён!', reply_markup=end_markup)
        admin(message)




bot.polling()