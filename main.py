import os
import webbrowser

import telebot

from telebot import types

bot = telebot.TeleBot(os.environ['TOKEN'])


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.gismeteo.ru/')


@bot.message_handler(commands=['start', 'main', 'hello'])
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
    markup.add(types.InlineKeyboardButton('Go to the web-site', url='https://www.google.com/'))
    markup.add(types.InlineKeyboardButton('Delete photo', callback_data="delete"))
    markup.add(types.InlineKeyboardButton('Edit text', callback_data="edit"))
    bot.reply_to(message, 'What a wonderful picture! Where was it taken?', reply_markup=markup)


bot.polling(none_stop=True)  # bot.infinity_polling() #another option
