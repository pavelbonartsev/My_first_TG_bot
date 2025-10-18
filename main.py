import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

token = '7206783181:AAEJZVB9YZXWnNTHPwi9HY1MInv9wBEc82w'
bot = telebot.TeleBot(token)

data_file = 'data.json'

def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def create_keyboard():
    keyboard = InlineKeyboardMarkup()
    button_start = InlineKeyboardButton("Старт", callback_data='start')
    button_help = InlineKeyboardButton("Помощь", callback_data='help')
    button_cezar = InlineKeyboardButton("Шифр Цезаря", callback_data='cezar')
    keyboard.add(button_start, button_help, button_cezar)
    return keyboard

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет!", reply_markup=create_keyboard())

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/start - старт работы с ботом\n/help - помощь\n/cezar - шифрование текста по шифру Цезаря\n", reply_markup=create_keyboard())

@bot.message_handler(commands=['cezar'])
def byCezar(message):
    bot.send_message(message.chat.id, "Введите текст...", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, cezar_2)

@bot.message_handler(content_types=['photo'])
def photo(message):   
    fileID = message.photo[-1].file_id   
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_photo(message.chat.id, downloaded_file)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'start':
        start_message(call.message)
    elif call.data == 'help':
        help(call.message)
    elif call.data == 'cezar':
        byCezar(call.message)

def cezar_2(message):
    user_data = load_data()
    user_id = message.from_user.id
    
    user_data[user_id] = message.text
    save_data(user_data)
    
    bot.send_message(message.chat.id, cezar(message.text))

def cezar(st):
    newSt = ""
    for i in st: 
        if i == "я":
            newSt += "а"
        elif i == "Я":
            newSt += "А"
        elif i == "Z":
            newSt += "A"
        elif i == "z":
            newSt += "а"
        else:
            newSt += chr(ord(i) + 1)
    return newSt

if __name__ == '__main__':
    bot.infinity_polling()
