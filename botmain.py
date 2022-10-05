import telebot
from telebot import types
import json

bot = telebot.TeleBot('5026433773:AAEO40Hv7kzNPffBHfX3DJT0RTf3SmkZF_k')
white_list = []
bilety = json.load(open("text.txt"))
temporary = {}


def answer_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 2
    markup.add(types.KeyboardButton('да, верно'),
               types.KeyboardButton('заполнить заново'))
    return markup


@bot.message_handler(commands=['start'])
def welcome(message):
    global bilety
    if message.chat.id == 970028914:
        if len(message.text) > 10:
            bot.reply_to(message, 'проверка билета {}'.format(bilety[message.text.split(' ')[1]]['bilet']))
            try:
                bot.send_photo(message.chat.id, bilety[message.text.split(' ')[1]]['photo'],
                               caption=bilety[message.text.split(' ')[1]]['name'] + '\n Билет купил этот человек')
            except:
                bot.send_message(message.chat.id, 'Билет не зарегестрирован')
        else:
            bot.reply_to(message, 'Бот предназначен для проверки билетов (Вы - охранник)')
    else:
        bot.reply_to(message, """\
        Бот для шабытовской хэлуинской тусы, подойдите к заполнению анкеты внимательно (фото и имя должны быть настоящими)""")
        if (bilety[message.text.split(' ')[1]]['chat_id'] == 0 or
            bilety[message.text.split(' ')[1]]['chat_id'] == message.chat.id) and bilety[message.text.split(' ')[1]][
            'chat_id'] != 'None':
            bilety[message.text.split(' ')[1]]['chat_id'] = message.chat.id
            global white_list
            white_list.append(message.chat.id)
            msg = bot.send_message(message.chat.id, "Ваш билет №{}".format(bilety[message.text.split(' ')[1]]['bilet'])
                                   + '\n\nВведите ваше имя')
            bot.register_next_step_handler(msg, step1)
            global temporary
            bilety[message.text.split(' ')[1]]['chat_id'] = message.chat.id
            temporary[message.chat.id] = {'name': 0, 'photo': 0, 'bilet': message.text.split(' ')[1]}
        elif bilety[message.text.split(' ')[1]]['chat_id'] == message.chat.id and bilety[message.text.split(' ')[1]][
            'name'] != 'None':
            bot.send_message(message.chat.id, "Вы уже зарегестрированы")
        else:
            bot.send_message(message.chat.id, 'Ваш билет занят')


@bot.message_handler(content_types=['text', 'photo'])
def step1(message):
    global temporary
    if temporary[message.chat.id]['name'] != 0 and temporary[message.chat.id]['photo'] != 0:
        bot.send_message(message.chat.id, 'Вы уже зарегестрированы, ожидайте дальнейших новостей')
    else:
        if message.chat.id in white_list:
            if message.content_type == 'text':
                # bilety[list(bilety.keys())[list(bilety.values()).index({'chat_id': message.chat.id})]]['name'] = message.text
                temporary[message.chat.id]['name'] = message.text
                msg = bot.send_message(message.chat.id, 'Пришлите Ваше фото ')
                bot.register_next_step_handler(msg, step2)


def step2(message):
    temporary[message.chat.id]['photo'] = message.photo[1].file_id
    msg = bot.send_photo(message.chat.id, temporary[message.chat.id]['photo'],
                         caption=temporary[message.chat.id][
                                     'name'] + '\n\n Данные введены верно? \n (Выберите вариант из предложенных)',
                         reply_markup=answer_markup())
    bot.register_next_step_handler(msg, step3)


def step3(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    if message.text == 'да, верно':
        bilety[temporary[message.chat.id]['bilet']]['name'] = temporary[message.chat.id]['name']
        bilety[temporary[message.chat.id]['bilet']]['photo'] = temporary[message.chat.id]['photo']
        msg = bot.send_message(message.chat.id, 'Поздравляем с покупкой билета', reply_markup=markup)
        json.dump(bilety, open("text.txt", 'w'))
    else:
        msg = bot.send_message(message.chat.id, 'Начинаем процедуру заново\n\nВведите Ваше имя', reply_markup=markup)
        bot.register_next_step_handler(msg, step1)


bot.infinity_polling()
