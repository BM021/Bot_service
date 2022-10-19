import telebot
from telebot import types

import database
import buttons

# Это демо версия бота!!!
bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    checker = database.check_client(user_id)
    if checker:
        bot.send_message(user_id, text='Выберите нужный пункт', reply_markup=buttons.main_menu_buttons())

    else:
        bot.send_message(user_id, 'Добро пожаловать!\nЭто Бот-асистент!\nОтправьте Юр. название компании')
        bot.register_next_step_handler(message, get_company_name)


def get_company_name(message):
    company_name = message.text

    bot.send_message(message.from_user.id, 'Отправьте свое имя')
    bot.register_next_step_handler(message, get_name, company_name)


def get_name(message, company_name):
    client_name = message.text

    bot.send_message(message.from_user.id, 'Отправьте телефон номер', reply_markup=buttons.phone_number_button())
    bot.register_next_step_handler(message, get_number, company_name, client_name)


def get_number(message, company_name, client_name):
    if message.contact:
        number = message.contact.phone_number

        bot.send_message(message.from_user.id, 'Отправьте Mail или Email', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_mail, company_name, client_name, number)
    else:
        bot.send_message(message.from_user.id, 'Отпрвавьте номер испоьзуя кнопку')
        bot.register_next_step_handler(message, get_number, client_name)


def get_mail(message, company_name, client_name, number):
    client_mail = message.text

    bot.send_message(message.from_user.id, 'Выберите услугу', reply_markup=buttons.services_buttons())
    bot.register_next_step_handler(message, get_work, company_name, client_name, number, client_mail)


def get_work(message, company_name, client_name, number, client_mail):
    work = message.text
    text = 'Введите дату когда будет старт проекта\n\nЕсли нету даты то нажмите "Пропустить"'

    bot.send_message(message.from_user.id, text, reply_markup=buttons.date_skip_button())
    bot.register_next_step_handler(message, get_date, company_name, client_name, number, client_mail, work)


def get_date(message, company_name, client_name, number, client_mail, work):
    date = message.text
    text = 'Введите деадлайн\n\nЕсли нету даты то нажмите "Пропустить"'

    bot.send_message(message.from_user.id, text, reply_markup=buttons.date_skip_button())
    bot.register_next_step_handler(message, get_deadline, company_name, client_name, number, client_mail, work, date)


def get_deadline(message, company_name, client_name, number, client_mail, work, date):
    deadline = message.text
    text = 'Выберите тип переговора\n\nЕсли нету то нажмите "Пропустить"'

    bot.send_message(message.from_user.id, text, reply_markup=buttons.meeting_buttons())
    bot.register_next_step_handler(message, get_meeting, company_name, client_name, number, client_mail, work, date,
                                   deadline)


def get_meeting(message, company_name, client_name, number, client_mail, work, date, deadline):
    meeting = message.text

    bot.send_message(message.from_user.id, 'Отправьте локацию', reply_markup=buttons.get_location_button())
    bot.register_next_step_handler(message, get_location, company_name, client_name, number, client_mail, work, date,
                                   deadline, meeting)


def get_location(message, company_name, client_name, number, client_mail, work, date, deadline, meeting):
    user_id = message.from_user.id
    admin_id = # your telegram id

    if message.location:
        user_location = (message.location.longitude, message.location.latitude)

        database.register_client(user_id, company_name, client_name, number, client_mail, work, date, deadline, meeting,
                                 user_location[0], user_location[1])

        client_text = 'Вы успешно подали заявку!\n\nС вами скоро свяжуться!'
        admin_text = f'Новый заказ от:\n\n{company_name}\n{client_name}\n{number}\n{work}'
        bot.send_message(user_id, client_text, reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(admin_id, admin_text)

    else:
        bot.send_message(message.from_user.id, 'Отправьте локацию используя кнопку')
        bot.register_next_step_handler(message, get_location, company_name, client_name, number, client_mail, work,
                                       date, deadline, meeting)


@bot.message_handler(commands=['admin'])
def admin_side(message):
    admin_id = # your telegram id

    if admin_id == message.from_user.id:
        bot.send_message(admin_id, 'Выберите нужный пункт', reply_markup=buttons.admin_side_buttons())


@bot.message_handler(content_types=['text'])
def text_messages(message):
    admin_id = # your telegram id

    if admin_id == message.from_user.id:
        if message.text == 'Удалить клиента':
            bot.send_message(admin_id, 'Выберите клиента', reply_markup=buttons.select_exact_client_button())
            bot.register_next_step_handler(message, get_exact_client_name)

        elif message.text == 'Изменить оплаты':
            bot.send_message(admin_id, 'Выберите нужный пункт', reply_markup=buttons.admin_choose_buttons())

        elif message.text == 'Ввести стоимость услуги':
            bot.send_message(admin_id, 'Выберите клиента', reply_markup=buttons.select_exact_client_button())
            bot.register_next_step_handler(message, get_client_name_to_set_service_price)

        elif message.text == 'Ввести оплату клиента':
            bot.send_message(admin_id, 'Выберите клиента', reply_markup=buttons.select_exact_client_button())
            bot.register_next_step_handler(message, get_client_name_to_set_payed)

        elif message.text == 'Назад':
            bot.send_message(admin_id, 'Вы вернулись назад', reply_markup=buttons.admin_side_buttons())

        else:
            bot.send_message(admin_id, 'Не понял')

    if message.from_user.id:
        if message.text == 'Наши контакты':
            bot.send_message(message.from_user.id, 'Наши контакты:\n\n+998909198801\n+998337218801')

        elif message.text == 'Где мы находимся':
            bot.send_message(message.from_user.id, 'Наш адрес: г.Ташкент, \nЯккасарайский район\n'
                                                   'Ул. Шота Руставели, Дом 2')


def get_exact_client_name(message):
    admin_id = # your telegram id
    delete_client_name = message.text

    database.delete_exact_client(delete_client_name)
    bot.send_message(admin_id, 'Клиент удален!', reply_markup=buttons.admin_side_buttons())


def get_client_name_to_set_service_price(message):
    admin_id = # your telegram id
    client_name = message.text

    bot.send_message(admin_id, 'Введите оплату клиента', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, client_service_price, client_name)


def client_service_price(message, client_name):
    admin_id = # your telegram id
    price = float(message.text)

    database.get_client_service_price(client_name, price)
    bot.send_message(admin_id, 'Успешно обновлено!', reply_markup=buttons.admin_choose_buttons())


def get_client_name_to_set_payed(message):
    admin_id = # your telegram id
    client_name = message.text

    bot.send_message(admin_id, 'Введите оплату клиента', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, client_payed, client_name)


def client_payed(message, client_name):
    admin_id = # your telegram id
    payed = float(message.text)

    database.update_client_payments(client_name, payed)
    bot.send_message(admin_id, 'Успешно обновлено!', reply_markup=buttons.admin_choose_buttons())


bot.polling()
