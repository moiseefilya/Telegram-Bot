import csv

import telebot
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()
bot = telebot.TeleBot(token=os.environ.get('TOKEN'))


application_list = []
MERCH_LIST = ['свитшот', 'футболка', 'толстовка']
SIZE_LIST = ['XS', 'S', 'M', 'L', 'XL', '2XL']
field_names = ['Продукт', 'Пол', 'Размер', 'Количество', 'ФИО', 'Контакты', 'Комментарий']


@bot.message_handler(commands=['start'])
def start(message):
    application_list.clear()
    mess = f'Привет, {message.from_user.first_name} \n\nВыбери нужный пункт:'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    product_name1 = types.KeyboardButton('Свитшот')
    product_name2 = types.KeyboardButton('Футболка')
    product_name3 = types.KeyboardButton('Толстовка')
    markup.add(product_name1, product_name2, product_name3)
    msg = bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, choose_merch)


def choose_merch(message):
    try:
        if message.text.lower() == 'футболка' or message.text.lower() == 'толстовка':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add('Мальчик', 'Девочка')
            msg = bot.send_message(message.chat.id, 'Мальчик или девочка?', reply_markup=markup)
            application_list.append(message.text)
            bot.register_next_step_handler(msg, choose_sex)
        elif message.text.lower() == 'свитшот':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
            size_xs = types.KeyboardButton('XS')
            size_s = types.KeyboardButton('S')
            size_m = types.KeyboardButton('M')
            size_l = types.KeyboardButton('L')
            size_xl = types.KeyboardButton('XL')
            size_2xl = types.KeyboardButton('2XL')
            markup.add(size_xs, size_s, size_m, size_l, size_xl, size_2xl)
            msg = bot.send_message(message.chat.id, 'Теперь определимся с размером:', reply_markup=markup)
            bot.register_next_step_handler(msg, choose_size)
            application_list.append(message.text)
            application_list.append('-')
        else:
            msg = bot.send_message(message.chat.id, 'Некорректный ввод, попробуйте снова')
            bot.register_next_step_handler(msg, choose_merch)
            return
    except Exception:
        bot.send_message(message, 'что то не так')


def choose_sex(message):
    sex = message.text
    try:
        if (sex.lower() != 'мальчик') and (sex.lower() != 'девочка'):
            msg = bot.send_message(message.chat.id, 'Некорректный ввод, попробуйте снова')
            bot.register_next_step_handler(msg, choose_sex)
            return
        application_list.append(sex)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
        size_xs = types.KeyboardButton('XS')
        size_s = types.KeyboardButton('S')
        size_m = types.KeyboardButton('M')
        size_l = types.KeyboardButton('L')
        size_xl = types.KeyboardButton('XL')
        size_2xl = types.KeyboardButton('2XL')
        markup.add(size_xs, size_s, size_m, size_l, size_xl, size_2xl)
        msg = bot.send_message(message.chat.id, 'Теперь определимся с размером:', reply_markup=markup)
        bot.register_next_step_handler(msg, choose_size)
    except Exception:
        bot.send_message(message, 'Что-то не так')


def choose_size(message):
    size = message.text.upper()
    try:
        if size not in SIZE_LIST:
            msg = bot.send_message(message.chat.id, 'Некорректный ввод, попробуйте снова')
            bot.register_next_step_handler(msg, choose_size)
            return
        application_list.append(size)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        one = types.KeyboardButton('1')
        two = types.KeyboardButton('2')
        three = types.KeyboardButton('3')
        other = types.KeyboardButton('...')
        markup.add(one, two, three, other)
        msg = bot.send_message(message.chat.id, 'Выберите количество:', reply_markup=markup)
        bot.register_next_step_handler(msg, choose_amount)
    except Exception:
        bot.send_message(message, 'Что-то не так')


def choose_amount(message):
    amount = message.text
    try:
        if amount == '0':
            msg = bot.send_message(message.chat.id, 'Нельзя заказать 0')
            bot.register_next_step_handler(msg, choose_amount)
            return
        elif amount == '...':
            msg = bot.send_message(message.chat.id, 'Введите число')
            bot.register_next_step_handler(msg, choose_amount)
            return
        elif not amount.isdigit():
            msg = bot.send_message(message.chat.id, 'Введите число')
            bot.register_next_step_handler(msg, choose_amount)
            return
        elif int(amount) < 0 or len(amount) > 2:
            msg = bot.send_message(message.chat.id, 'Это слишком много...')
            bot.register_next_step_handler(msg, choose_amount)
            return
        application_list.append(str(amount))
        msg = bot.send_message(message.chat.id, 'Введите ФИО')
        bot.register_next_step_handler(msg, process_name)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так')


def process_name(message):
    name = message.text
    result = len(name.split())
    try:
        if result not in [2, 3]:
            msg = bot.send_message(message.chat.id, 'Некорректный ввод данных, попробуйте снова')
            bot.register_next_step_handler(msg, process_name)
            return
        application_list.append(name)
        msg = bot.send_message(message.chat.id, 'Введите контакт (номер тел/tg/почта):')
        bot.register_next_step_handler(msg, process_contact)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так')


def process_contact(message):
    try:
        cont = message.text
        application_list.append(str(cont))
        msg = bot.send_message(message.chat.id, 'Введите комментарий к заказу (либо "-")')
        bot.register_next_step_handler(msg, process_comm)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так')


def process_comm(message):
    try:
        comm = message.text
        application_list.append(comm)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        ans1 = types.KeyboardButton('Да')
        ans2 = types.KeyboardButton('Нет')
        markup.add(ans1, ans2)
        bot.send_message(message.chat.id, 'Ваш заказ:')
        bot.send_message(message.chat.id,
                                f'<u>Продукт:</u> {application_list[1]}\n<u>Пол:</u> {application_list[2]}\n'
                                f'<u>Размер:</u> {application_list[3]}\n<u>Кол-во:</u> {application_list[4]}\n'
                                f'<u>ФИО:</u> {application_list[5]}\n<u>Контакт:</u> {application_list[6]}\n'
                                f'<u>Комментарий:</u> {application_list[7]}',
                                parse_mode='html')
        msg = bot.send_message(message.chat.id, 'Вы уверены что хотите сделать заказ?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_proof)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так')


def process_proof(message):
    answer = message.text.lower()
    try:
        if answer == 'да' or answer == 'уверен':
            bot.send_message(message.chat.id, 'Спасибо за заказ!\nДля заказа снова используйте /start')
            with open('shopping_list.csv', 'a', encoding='utf-8', newline='') as f:
                if os.stat('shopping_list.csv').st_size == 0:
                    writer = csv.writer(f)
                    writer.writerow(field_names)
                    writer.writerow(application_list)
                else:
                    writer = csv.writer(f)
                    writer.writerow(application_list)
        else:
            bot.send_message(message.chat.id, 'Ваш заказ отменен, для заказа снова используйте /start')
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так')


bot.polling(none_stop=True)
