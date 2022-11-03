import requests
import telebot
from PIL import Image
from telebot import types
import json

TOKEN = '5026433773:AAEO40Hv7kzNPffBHfX3DJT0RTf3SmkZF_k'
bot = telebot.TeleBot(TOKEN)
white_list = {}
bilety = json.load(open("text.txt"))
temporary = {}


def answer_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 2
    markup.add(types.KeyboardButton('да, верно'),
               types.KeyboardButton('заполнить заново'))
    return markup


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """\
            За помощью можно обратиться к @spookyshot""")


@bot.message_handler(commands=['start'])
def welcome(message):
    global bilety
    global temporary
    if message.chat.id == 9728914:
        if len(message.text) > 10:
            bot.reply_to(message, 'проверка билета {}'.format(bilety[message.text.split(' ')[1]]['bilet']))
            try:
                if bilety[message.text.split(' ')[1]]['checked'] == 0:
                    bot.send_photo(message.chat.id, bilety[message.text.split(' ')[1]]['photo'],
                                   caption=bilety[message.text.split(' ')[1]]['name']
                                           + '\n БИЛЕТ №{}'.format(bilety[message.text.split(' ')[1]]['bilet'])
                                           + '\n Билет купил этот человек')
                    bilety[message.text.split(' ')[1]]['checked'] = 1
                    json.dump(bilety, open("text.txt", 'w'))
                else:
                    bot.send_photo(message.chat.id, bilety[message.text.split(' ')[1]]['photo'],
                                   caption=bilety[message.text.split(' ')[1]][
                                               'name'] + '\n БИЛЕТ №{}'.format(bilety[message.text.split(' ')[1]][
                                                                                   'bilet']) + '\n Билет купил этот человек \n\n Человек уже прошел вход')
            except:
                bot.send_message(message.chat.id, 'Билет не зарегестрирован')
        else:
            bot.reply_to(message, 'Бот предназначен для проверки билетов (Вы - охранник)')
    else:
        bot.reply_to(message, """\
        Добро пожаловать в бот SPOOKYSHOT PARTY""")
        if len(message.text) > 10:
            if bilety[message.text.split(' ')[1]]['chat_id'] == 0:
                bilety[message.text.split(' ')[1]]['chat_id'] = message.chat.id
                global white_list
                bot.send_message(message.chat.id,
                                 "Подойдите к заполнению анкеты внимательно(фото и имя должны быть настоящими)")
                white_list[message.chat.id] = message.text.split(' ')[1]
                msg = bot.send_message(message.chat.id,
                                       "Ваш билет №{}".format(bilety[message.text.split(' ')[1]]['bilet'])
                                       + '\n\nВведите Ваше имя')
                bot.register_next_step_handler(msg, step1)
                bilety[message.text.split(' ')[1]]['chat_id'] = message.chat.id
                temporary[message.chat.id] = {'name': 0, 'photo': 0, 'bilet': message.text.split(' ')[1]}
            elif bilety[message.text.split(' ')[1]]['chat_id'] == message.chat.id and \
                    bilety[message.text.split(' ')[1]][
                        'name'] != 'None':
                bot.send_message(message.chat.id, "Вы уже зарегестрированы")
            elif bilety[message.text.split(' ')[1]]['chat_id'] == 'Blocked':
                bot.send_message(message.chat.id, "Этот билет был вернут, идите нахуй, наебать не прокатит")
            else:
                bot.send_photo(message.chat.id, bilety[message.text.split(' ')[1]]['photo'],
                               caption=bilety[message.text.split(' ')[1]][
                                           'name'] + '\n Билет купил этот человек')


@bot.message_handler(content_types=['text', 'photo'])
def step1(message):
    global temporary
    if message.chat.id == 1253815359:
        if message.text == 'Статистика':
            j = 0
            x = 0
            for i in list(bilety.keys()):
                if bilety[i]['checked'] == 1:
                    j = j + 1
                if bilety[i]['name'] != 'None':
                    x = x + 1
            bot.send_message(message.chat.id, 'вход прошло: ' + str(j) + '\n\n зарегестрировано: ' + str(x) + '\n\n')
        elif message.text.startswith('Удалить'):
            nomer = message.text.split(' ')[1]
            for i in list(bilety.keys()):
                if bilety[i]['bilet'] == nomer and bilety[i]['name'] != 'None':
                    bilety[i] = {'bilet': nomer, 'name': 'None', 'photo': 'None', 'chat_id': 'Blocked', 'checked': 0}
                    json.dump(bilety, open("text.txt", 'w'))
                    bot.send_message(message.chat.id, 'Билет {} был успешно возвращен'.format(nomer))
        elif message.text.startswith('Заново'):
            nomer = message.text.split(' ')[1]
            for i in list(bilety.keys()):
                if bilety[i]['bilet'] == nomer and bilety[i]['name'] != 'None':
                    bilety[i] = {'bilet': nomer, 'name': 'None', 'photo': 'None', 'chat_id': 0, 'checked': 0}
                    json.dump(bilety, open("text.txt", 'w'))
        elif message.text.startswith('Рассылка::'):
            for i in list(bilety.keys()):
                chat = bilety[i]['chat_id']
                if chat != 0 and chat != 'Blocked':
                    bot.send_message(chat, message.text.split('::')[1])
        elif message.text == 'Конкурс':
            import random
            a = 0
            while a == 0:
                winner = str(random.randint(1, 200))
                for i in list(bilety.keys()):
                    if bilety[i]['bilet'] == winner and (
                            bilety[i]['chat_id'] != 0 and bilety[i]['chat_id'] != "Blocked"):
                        print(winner)
                        bot.send_photo(message.chat.id, bilety[i]['photo'],
                                       caption=bilety[i][
                                                   'name'] + '\n БИЛЕТ №{} \nПобедил этот человек'.format(winner))
                        bot.send_message(bilety[i]['chat_id'],
                                         'БИЛЕТ №{} ТЫ ПОБЕДИЛ В КОНКУРСЕ, НАЙДИ ИСУСА И ЗАБЕРИ ПРИЗ'.format(winner))
                        a = 1
                        break
                    else:
                        continue


    elif message.chat.id not in list(white_list.keys()):
        bot.send_message(message.chat.id, 'Вся инфа по тусовке (https://www.instagram.com/spookyshot.party/)')
    elif temporary[message.chat.id]['name'] != 0 and temporary[message.chat.id]['photo'] != 0:
        bot.send_message(message.chat.id, 'Вы уже зарегестрированы, ожидайте дальнейших новостей')
    else:
        if message.chat.id in list(white_list.keys()):
            if message.content_type == 'text':
                # bilety[list(bilety.keys())[list(bilety.values()).index({'chat_id': message.chat.id})]]['name'] = message.text
                temporary[message.chat.id]['name'] = message.text
                msg = bot.send_message(message.chat.id, 'Пришлите Ваше фото ')
                bot.register_next_step_handler(msg, step2)


def step2(message):

    if message.photo != None:
        temporary[message.chat.id]['photo'] = message.photo[1].file_id
        # get URL by id
        file_path = \
            requests.get(
                f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={temporary[message.chat.id]["photo"]}').json()[
                'result'][
                'file_path']
        img = Image.open(requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_path}', stream=True).raw)
        img.save('photos/photo{}.jpg'.format(bilety[temporary[message.chat.id]['bilet']]['bilet']))
        msg = bot.send_photo(message.chat.id, temporary[message.chat.id]['photo'],
                             caption=temporary[message.chat.id][
                                         'name'] + '\n\n Данные введены верно? \n (Выберите вариант из предложенных)',
                             reply_markup=answer_markup())
        bot.register_next_step_handler(msg, step3)
    else:
        msg = bot.send_message(message.chat.id, 'Пришлите Ваше фото ')
        bot.register_next_step_handler(msg, step3)


def step3(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    if message.text == 'да, верно':
        bilety[temporary[message.chat.id]['bilet']]['name'] = temporary[message.chat.id]['name']
        bilety[temporary[message.chat.id]['bilet']]['photo'] = temporary[message.chat.id]['photo']
        bilety[temporary[message.chat.id]['bilet']]['checked'] = 0
        msg = bot.send_message(message.chat.id, 'Билет был куплен, ожидайте дальнейших новостей', reply_markup=markup)
        json.dump(bilety, open("text.txt", 'w'))
        json.dump(white_list, open("chats.txt", 'w'))
    else:
        msg = bot.send_message(message.chat.id, 'Начинаем процедуру регитрации заново\n\nВведите Ваше имя',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, step1)


bot.infinity_polling()
