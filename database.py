import sqlite3
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credents.json", scope)

client = gspread.authorize(creds)

table = client.open("Work")
list_1 = table.worksheet("Лист1")


connection = sqlite3.connect('work.db')
sql = connection.cursor()
sql.execute('CREATE TABLE IF NOT EXISTS clients ('
            'telegram_id INTEGER, company_name TEXT, client_name TEXT, number TEXT, mail TEXT, work TEXT, date TEXT,'
            'deadline TEXT, meeting TEXT, longitude REAL, latitude REAL, price REAL, payed REAL, must_pay REAL,'
            'reg_date DATETIME);')


def check_client(telegram_id):
    connection = sqlite3.connect('work.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT telegram_id FROM clients WHERE telegram_id =?', (telegram_id,)).fetchone()

    if checker:
        return True

    else:
        return False


# Регистрация клиента
def register_client(telegram_id, company_name, client_name, number, mail, work,
                    date, deadline, meeting, longitude, latitude, price=0, payed=0, must_pay=0):

    connection = sqlite3.connect('work.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                (telegram_id, company_name, client_name, number, mail, work,
                    date, deadline, meeting, longitude, latitude, price, payed, must_pay, datetime.now()))

    list_1.append_row([telegram_id, company_name, client_name, number, mail, work,
                    date, deadline, meeting, longitude, latitude, price, payed, must_pay, str(datetime.now())])

    connection.commit()


# Получить конкретного клиента
def get_exact_clients(number):
    connection = sqlite3.connect('work.db')
    sql = connection.cursor()

    exact_client = sql.execute('SELECT company_name, client_name, number, mail WHERE number=?;', (number,)).fetchone()

    return exact_client


# Получение всех клиентов
def get_all_clients_names():
    connection = sqlite3.connect('work.db')
    sql = connection.cursor()

    clients = sql.execute('SELECT client_name FROM clients;').fetchall()
    get_clients = [i[0] for i in clients]

    return get_clients


# Админ панель, Удаление клиента из базы
def delete_exact_client(client_name):
    connection = sqlite3.connect('work.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM clients WHERE client_name=?;', (client_name,))
    connection.commit()

    delete_client = list_1.find(client_name)
    if delete_client:
        list_1.delete_rows(delete_client.row)
    else:
        return False


# Админ панель, Изменение стоимость услуги конкрениного клиента
def get_client_service_price(name, price):
    connection = sqlite3.connect('work.db')
    sql = connection.cursor()

    sql.execute('UPDATE clients SET price=? WHERE client_name=?;', (price, name))
    connection.commit()

    cell = list_1.find(name)
    if cell:
        list_1.update(f'L{cell.row}', price)
    else:
        return False


# Админ панель, Изменение оплаты конкрениного клиента
def update_client_payments(name, payed):
    connection = sqlite3.connect('work.db')
    sql = connection.cursor()

    a = sql.execute('SELECT price FROM clients WHERE client_name=?', (name,)).fetchone()
    b = sql.execute('SELECT payed FROM clients WHERE client_name=?', (name,)).fetchone()

    a = a[0]
    b = b[0]

    if a == b:
        text = 'Цена и оплата равны!'
        return text

    else:

        if b == 0.0:
            must_pay = a-payed

            sql.execute('UPDATE clients SET payed=?, must_pay=? WHERE client_name=?;', (payed, must_pay, name))
            connection.commit()

            cell = list_1.find(name)
            list_1.update(f'M{cell.row}', b)
            list_1.update(f'N{cell.row}', must_pay)

        else:
            client_payed = b+payed
            must_pay = client_payed - a

            sql.execute('UPDATE clients SET payed=?, must_pay=? WHERE client_name=?;', (client_payed, must_pay, name))
            connection.commit()

            cell = list_1.find(name)
            list_1.update(f'M{cell.row}', b)
            list_1.update(f'N{cell.row}', must_pay)
