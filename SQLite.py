# -*- coding: cp1251 -*-

import sqlite3
import os
import json
from datetime import datetime


def createtable() -> None:
    '''Создание таблицы в базе данных.
       Аргументы: None
       Возвращает: status (bool)
    '''
    cursor.execute(''' CREATE TABLE IF NOT EXISTS 'Cookie Profile'
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    data_creation_timedata TEXT NOT NULL,
    cookie TEXT,
    last_using_timedata TEXT,
    using_count INTEGER);''')
    print('Создана БД БД Profile.db.'
          'Создана таблица Cookie Profile в БД Profile.db')


def datainsert(n: int) -> None:
    '''Добавление n первых строк в таблицу БД.
       Аргументы:
       n - количество строк (int)
       Возвращает: None
    '''
    try:
        data_to_insert = str(datetime.now())
        for i in range(n):
            cursor.execute('''INSERT INTO 'Cookie Profile'
                              (data_creation_timedata)VALUES (?);''',
                              (data_to_insert,)
                           )
        print(f'Добавлены дата и время в количестве {n} строк '
              'в таблицу Cookie Profile.')
    except:
        pass


def showdbtable() -> list:
    '''Выводит в консоль содержимое таблицы 'Cookie Profile'
       Аргументы: None
       Возвращает: Список из строк БД (list)
    '''
    connection = sqlite3.connect('Profile.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT * FROM 'Cookie Profile';''')
    result = cursor.fetchall()
    for i in result:
        print(i)
    return result


def incert_cookies_in_db(cookies: list, id: int) -> None:
    '''Добавляет в cookies в БД
       Аргументы:
       cookies: list
       id: int
       Возвращает: None
    '''
    connection = sqlite3.connect('Profile.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE 'Cookie Profile' SET cookie = ? WHERE id = ?;", (cookies, id,))
    connection.commit()
    connection.close()
    last_run_update(id)


def get_cookies_from_db() -> list:
    '''Возвращает из БД все cookies в виде списка словарей.
       Аргументы: None
       Возвращает: cookie_list (список словарей с cookies)
       cookie_list = [dict, dict, dict...]
    '''
    cookie_list = []
    connection = sqlite3.connect('Profile.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT cookie FROM 'Cookie Profile';''')
    cookie_data_from_db = cursor.fetchall()
    connection.commit()
    connection.close()
    try:
        for cookie_string in cookie_data_from_db:
            if cookie_string[0] is not None:
                cookie_dict = json.loads(cookie_string[0][1:-1].split(', {"domain":')[0])
                cookie_list.append(cookie_dict)
    except:
        pass
    return cookie_list


def last_run_update(id: int) -> None:
    '''Обновляет в БД:
       1. Время последнего посещения
       2. Количество оращений к БД
       Аргументы: id: int (id обновленной строки)
       Возвращает: None
    '''
    connection = sqlite3.connect('Profile.db')
    cursor = connection.cursor()
    now = datetime.now()
    cursor.execute("UPDATE 'Cookie Profile' SET last_using_timedata = ? WHERE id = ?;", (now, id,))
    cursor.execute("SELECT using_count FROM 'Cookie Profile' WHERE id = ?;", (id,))
    result = cursor.fetchall()[0][0]
    if result is None:
        count = 1
    else:
        count = result + 1
    cursor.execute("UPDATE 'Cookie Profile' SET using_count = ? WHERE id = ?;", (count, id,))
    connection.commit()
    connection.close()


def main_process() -> list:
    '''Создаеь БД и таблицу, если их еще нет, добавялет строки
       в таблицу, возвращает список строк в БД.
       Аргументы: None
       Возвращает: Список из строк БД (list)
    '''
    global cursor
    if os.path.isfile("Profile.db"):
        pass
    else:
        connection = sqlite3.connect('Profile.db')  # Cоздаем/коннектимся к БД
        cursor = connection.cursor()  # Инициализируем подключение к БД
        createtable()  # Cоздаем таблицу в БД
        datainsert(n=15)  # Заполняем первые n строк таблицы в БД
        connection.commit()  # Сохраняем изменения
        connection.close()  # Закрываем соединение с БД
    result_list = showdbtable()
    return result_list


if __name__ == '__main__':
    main_process()
