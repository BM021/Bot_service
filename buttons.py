from telebot import types
import database


def main_menu_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_1 = types.KeyboardButton('Наши контакты')
    button_2 = types.KeyboardButton('Где мы находимся')

    kb.add(button_1, button_2)

    return kb


# Копки регистрации
def phone_number_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone_number = types.KeyboardButton('Отправить контакт', request_contact=True)
    kb.add(phone_number)

    return kb


def get_location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Отправить локацию', request_location=True)
    kb.add(location)

    return kb


# Кнопки админа
def admin_side_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_1 = types.KeyboardButton('Удалить клиента')
    button_2 = types.KeyboardButton('Изменить оплаты')

    kb.add(button_2, button_1)

    return kb


def admin_choose_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_1 = types.KeyboardButton('Ввести стоимость услуги')
    button_2 = types.KeyboardButton('Ввести оплату клиента')
    button_3 = types.KeyboardButton('Назад')

    kb.add(button_1, button_2, button_3)

    return kb


def select_exact_client_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    got_clients = database.get_all_clients_names()

    for client in got_clients:
        kb.add(client)

    return kb


def services_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Разработка телеграмм-ботов')
    button_2 = types.KeyboardButton('Разработка сайтов (Backend)')
    button_3 = types.KeyboardButton('Разработка сайтов (Frontend)')
    button_4 = types.KeyboardButton('Другое')

    kb.add(button_1, button_2, button_3, button_4)

    return kb


def date_skip_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    skip_button = types.KeyboardButton('Пропустить')
    kb.add(skip_button)

    return kb


def meeting_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton('Встреча')
    button_2 = types.KeyboardButton('По телефону')
    button_3 = types.KeyboardButton('Онлайн (Zoom)')
    button_4 = types.KeyboardButton('Пропустить')

    kb.row(button_3)
    kb.add(button_1, button_2)
    kb.row(button_4)

    return kb
