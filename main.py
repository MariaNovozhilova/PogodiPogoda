import os
import webbrowser
import sqlite3
import telebot

from telebot import types

bot = telebot.TeleBot(os.environ['TOKEN'])
name = None

@bot.message_handler(commands = ['start'])

def start(message):
    conn = sqlite3.connect('pogodipogoda.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Hello, you're going to be registered. Please, enter your name.")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Hello, you're going to be registered. Please, enter your password.")
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('pogodipogoda.sql')
    cur = conn.cursor()

    cur.execute(
        f'INSERT INTO users (name, pass) VALUES ({name}, {password})')
    conn.commit()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton)
    bot.send_message(message.chat.id, "The user has been registered.")

    #bot.send_message(message.chat.id, "Hello, you're going to be registered. Please, enter your password.")
    #bot.register_next_step_handler(message, user_pass)



# этот код сразу на старте предлагает кнопки, здоровается и высылает картинку
#    markup = types.ReplyKeyboardMarkup()
#    btn1 = types.KeyboardButton('Go to the web-site')
#    markup.row(btn1)
#    btn2 = types.KeyboardButton('Delete photo')
#    btn3 = types.KeyboardButton('Edit text')
#    markup.row(btn2, btn3)
#    file = open('./photo.jpg', 'rb')
#    bot.send_photo(message.chat.id, file, reply_markup=markup)
#    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name} 💋', reply_markup=markup)
#    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Go to the web-site':
        bot.send_message(message.chat.id, 'Website is open')
    elif message.text == 'Delete photo':
        bot.send_message(message.chat.id, 'Delete')

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.gismeteo.ru/')


@bot.message_handler(commands=['main', 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'Hi there, {message.from_user.first_name}  {message.from_user.last_name}')


@bot.message_handler(commands=['why?'])
def main(message):
    bot.send_message(message.chat.id, "<b><u>Nature</u></b> <em>did it.</em>", parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'hi':
        bot.send_message(message.chat.id, f'Hi there, {message.from_user.first_name}  {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Go to the web-site', url='https://www.google.com/')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Delete photo', callback_data="delete")
    btn3 = types.InlineKeyboardButton('Edit text', callback_data="edit")
    markup.row(btn2, btn3)

    bot.reply_to(message, 'What a wonderful picture! Where was it taken?', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1) #when btn is pressed, the previous message is deleted
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

bot.polling(none_stop=True)  # bot.infinity_polling() #another option
