import telebot
import os
from dotenv import load_dotenv
from telebot import types


load_dotenv()
bot = telebot.TeleBot(token=os.environ.get('TOKEN'))


application_list = []
MERCH_LIST = ['Cвитшот', 'Футболка', 'Толстовка']
SIZE_LIST = ['XS', 'S', 'M', 'L', 'XL', '2XL']
AMOUNT_LIST = ['1', '2', '3', '4', '5', '...']


@bot.message_handler(commands=['start'])
def start(message):
    application_list.clear()
    mess = f'Привет, {message.from_user.first_name} \n\nВыбери нужный пункт:'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for x in  MERCH_LIST:
        markup.add(types.KeyboardButton(x))
    msg = bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, choose_merch)


def choose_merch(message):
    try:
        if message.text not in MERCH_LIST:
            msg = bot.send_message(message.chat.id, 'Некорректный ввод, попробуйте снова')
            bot.register_next_step_handler(msg, choose_merch)
            return
        elif message.text.lower() == 'футболка' or message.text.lower() == 'толстовка':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add('Мальчик', 'Девочка')
            msg = bot.send_message(message.chat.id, 'Мальчик или девочка?', reply_markup=markup)
            bot.register_next_step_handler(msg, choose_sex)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
            for x in  SIZE_LIST:
                markup.add(types.KeyboardButton(x))
            msg = bot.send_message(message.chat.id, 'Теперь определимся с размером:', reply_markup=markup)
            bot.register_next_step_handler(msg, choose_size)
        application_list.append(message.text)
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
        for x in  SIZE_LIST:
            markup.add(types.KeyboardButton(x))
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5, one_time_keyboard=True)
        for x in  AMOUNT_LIST:
            markup.add(types.KeyboardButton(x))
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
        msg = bot.send_message(message.chat.id, 'Введите учебную группу (либо "-"):')
        bot.register_next_step_handler(msg, process_group)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так')


def process_group(message):
    try:
        group = message.text
        application_list.append(str(group))
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
        msg = bot.send_message(message.chat.id, 'Вы уверены что хотите сделать заказ?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_proof)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так')


def process_proof(message):
    answer = message.text.lower()
    try:
        if answer == 'да' or answer == 'уверен':
            bot.send_message(message.chat.id, 'Спасибо за заказ!\nДля заказа снова используйте /start')
            if application_list[0].lower() == 'футболка' or application_list[0].lower() == 'толстовка':
                bot.send_message(541081425,
                                 f' <u>Продукт:</u> {application_list[0]}\n<u>Пол:</u> {application_list[1]}\n'
                                 f'<u>Размер:</u> {application_list[2]}\n<u>Кол-во:</u> {application_list[3]}\n'
                                 f'<u>ФИО:</u> {application_list[4]}\n<u>Группа:</u> {application_list[5]}\n'
                                 f'<u>Контакт:</u> {application_list[6]}\n<u>Комментарий:</u> {application_list[7]}',
                                 parse_mode='html')
            else:
                bot.send_message(541081425,
                                 f' <u>Продукт:</u> {application_list[0]}\n<u>Размер:</u> {application_list[1]}\n'
                                 f'<u>Кол-во:</u> {application_list[2]}\n<u>ФИО:</u> {application_list[3]}\n'
                                 f'<u>Группа:</u> {application_list[4]}\n<u>Контакт:</u> {application_list[5]}\n'
                                 f'<u>Комментарий:</u> {application_list[6]}',
                                 parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Ваш заказ отменен, для заказа снова используйте /start')
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так')


bot.polling(none_stop=True)
