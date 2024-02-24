import os
import webbrowser
import sqlite3
import telebot
import requests
import json
from currency_converter import CurrencyConverter
import datetime
from telebot import types
bot = telebot.TeleBot(os.environ['TOKEN'])
API = os.environ['API']
name = None
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands = ['start','main'])
def start(message):
    print(f'start called by {message.from_user.first_name}')
    now = datetime.datetime.now().hour
    print(now)
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Currency Calc')
    btn2 = types.KeyboardButton('Weather Today')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Chat on everything')
    markup.row(btn3)
    file = open('./Start Photo.png', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    if now >= 0 and now < 4: # depending on the current time, the bot chooses a greeting
        bot.send_message(message.chat.id,
                         f"Good night, {message.from_user.first_name} {message.from_user.last_name} 💋. \n")
    elif (4 <= now <= 11):
        bot.send_message(message.chat.id, f"Good morning, {message.from_user.first_name} {message.from_user.last_name} 💋. \n")
    elif 11 < now < 17:
        bot.send_message(message.chat.id,f"Good afternoon, {message.from_user.first_name} {message.from_user.last_name} 💋. \n")
    elif 17 <= now: bot.send_message(message.chat.id,
                             f"Good night, {message.from_user.first_name} {message.from_user.last_name} 💋. \n")

    bot.send_message(message.chat.id, f"I'm PogodiPogoda Bot. Choose a button or just talk to me.", reply_markup=markup)
    bot.register_next_step_handler(message, where_to_go)

@bot.message_handler(content_types='text')
def start2(message):
    markup = types.ReplyKeyboardMarkup()  # этот код сразу на старте предлагает кнопки, здоровается и высылает картинку
    btn1 = types.KeyboardButton('Currency Calc')
    btn2 = types.KeyboardButton('Weather Today')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Chat about everything')
    markup.row(btn3)
    bot.send_message(message.chat.id, f"Hi again, {message.from_user.first_name} {message.from_user.last_name}. \n"
                                      f"I'm ready to continue. Choose a button or just talk to me.",
                     reply_markup=markup)
    bot.register_next_step_handler(message, where_to_go)

def where_to_go(message):
    print(f'where_to_go called by {message.from_user.first_name}')
    nowdate = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print(nowdate)
    question = message.text.lower()
    print(question)
    print(type(question))

    if message.text == 'Currency Calc':
       converter(message)
    elif message.text == 'Weather Today':
        city(message)
    else:
#        bot.reply_to(message, "Let me think")
        if message.text.lower() in ['site', 'website']:
            webbrowser.open('https://www.gismeteo.ru/')
        elif message.text.lower() in ['hello', 'hi']:
            bot.send_message(message.chat.id,
                             f'Hi there, {message.from_user.first_name}  {message.from_user.last_name}')
        elif 'why' in question.split():
            bot.send_message(message.chat.id, "<b><u>Nature</u></b> <em>did it.</em>", parse_mode='html')
        elif message.text.lower() == 'id':
            bot.reply_to(message, f'ID: {message.from_user.id}')
        else:
            bot.send_message(message.chat.id, "I have nothing to say.")
        bot.send_message(message.chat.id, "If you want to know more, please register.")
        bot.register_next_step_handler(message, registration)

conn = sqlite3.connect('pogodipogoda.sql')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
conn.commit()
conn.close()

def registration(message):
    bot.send_message(message.chat.id, "Hello, you're going to be registered. Please, enter your name.")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
     global name
     name = message.text.strip()
     conn = sqlite3.connect('pogodipogoda.sql')
     cur = conn.cursor()
     cur.execute(
               "INSERT INTO users (name) VALUES ('%s')" % (name))
     conn.commit()
     cur.close()
     conn.close()
     bot.send_message(message.chat.id, "Thank you for registration. "
                                       "I want to tell you who has also registered")
     bot.register_next_step_handler(message, userlist)
     bot.register_next_step_handler(message, start2)

# def user_pass(message):
#      password = message.text.strip()
#
#      conn = sqlite3.connect('pogodipogoda.sql')
#      cur = conn.cursor()
#
#      cur.execute(
#          "INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
#      conn.commit()
#      cur.close()
#      conn.close()

   # markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton('Users list', callback_data='users'))
    # bot.send_message(message.chat.id, "The user has been registered.", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call:True) # here we retrieve the users list from the db and show it
def userlist(message):
    conn = sqlite3.connect('pogodipogoda.sql')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall() # returns all records found

    info = ''
    for el in users:
        info += f'Name: {el[1]}, pass: {el[2]}\n'
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info)


# def on_click(message):
#     if message.text == 'Go to the web-site':
#         bot.send_message(message.chat.id, 'Website is open')
#     elif message.text == 'Delete photo':
#         bot.send_message(message.chat.id, 'Delete')

def city(message):
    print(f'city called by {message.from_user.first_name}')
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Moscow')
    btn2 = types.KeyboardButton('Saint Petersburg')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Nizhny Novgorod')
    markup.row(btn3)
    bot.send_message(message.chat.id, f"Hi, {message.from_user.first_name} {message.from_user.last_name} 💋. \n"
                                      f"Choose a city, please, or write a city name.", reply_markup=markup)
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    print(f'get_weather called by {message.from_user.first_name}')
    city = message.text.strip().lower().replace(" ","+")
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'The temperature is {temp} C')
        image = 'snow.png' if temp > 5.0 else 'Sun.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
        bot.register_next_step_handler(message, start2)
    else:
        bot.reply_to(message, 'Wrong city name')
        bot.register_next_step_handler(message, start2)
    return


@bot.message_handler(commands=['convert'])
def converter (message):
    bot.send_message(message.chat.id, 'Hi, please enter the amount:')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'A number is expected, try again.')
        bot.register_next_step_handler(message, start2)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data = 'usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Other', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Choose the currencies', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'A number must be positive')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Amounts to {round(res, 2)}. You can enter new amount.')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Enter the currencies via /')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Amounts to {round(res, 2)}. You can enter new amount.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f"Something is wrong. Write correct currencies' names via /.")
        bot.register_next_step_handler(message, my_currency)
# @bot.message_handler(content_types=['photo'])
# def get_photo(message):
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton('Go to the web-site', url='https://www.google.com/')
#     markup.row(btn1)
#     btn2 = types.InlineKeyboardButton('Delete photo', callback_data="delete")
#     btn3 = types.InlineKeyboardButton('Edit text', callback_data="edit")
#     markup.row(btn2, btn3)
#
#     bot.reply_to(message, 'What a wonderful picture! Where was it taken?', reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
#     if callback.data == 'delete':
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1) #when btn is pressed, the previous message is deleted
#     elif callback.data == 'edit':
#         bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

bot.polling(none_stop=True)  # bot.infinity_polling() #another option
