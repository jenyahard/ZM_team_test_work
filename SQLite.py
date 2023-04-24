# -*- coding: cp1251 -*-

import sqlite3
import os
import json
from datetime import datetime


def createtable() -> None:
    '''�������� ������� � ���� ������.
       ���������: None
       ����������: status (bool)
    '''
    cursor.execute(''' CREATE TABLE IF NOT EXISTS 'Cookie Profile'
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    data_creation_timedata TEXT NOT NULL,
    cookie TEXT,
    last_using_timedata TEXT,
    using_count INTEGER);''')
    print('������� �� �� Profile.db.'
          '������� ������� Cookie Profile � �� Profile.db')


def datainsert(n: int) -> None:
    '''���������� n ������ ����� � ������� ��.
       ���������:
       n - ���������� ����� (int)
       ����������: None
    '''
    try:
        data_to_insert = str(datetime.now())
        for i in range(n):
            cursor.execute('''INSERT INTO 'Cookie Profile'
                              (data_creation_timedata)VALUES (?);''',
                              (data_to_insert,)
                           )
        print(f'��������� ���� � ����� � ���������� {n} ����� '
              '� ������� Cookie Profile.')
    except:
        pass


def showdbtable() -> list:
    '''������� � ������� ���������� ������� 'Cookie Profile'
       ���������: None
       ����������: ������ �� ����� �� (list)
    '''
    connection = sqlite3.connect('Profile.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT * FROM 'Cookie Profile';''')
    result = cursor.fetchall()
    for i in result:
        print(i)
    return result


def incert_cookies_in_db(cookies: list, id: int) -> None:
    '''��������� � cookies � ��
       ���������:
       cookies: list
       id: int
       ����������: None
    '''
    connection = sqlite3.connect('Profile.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE 'Cookie Profile' SET cookie = ? WHERE id = ?;", (cookies, id,))
    connection.commit()
    connection.close()
    last_run_update(id)


def get_cookies_from_db() -> list:
    '''���������� �� �� ��� cookies � ���� ������ ��������.
       ���������: None
       ����������: cookie_list (������ �������� � cookies)
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
    '''��������� � ��:
       1. ����� ���������� ���������
       2. ���������� �������� � ��
       ���������: id: int (id ����������� ������)
       ����������: None
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
    '''������� �� � �������, ���� �� ��� ���, ��������� ������
       � �������, ���������� ������ ����� � ��.
       ���������: None
       ����������: ������ �� ����� �� (list)
    '''
    global cursor
    if os.path.isfile("Profile.db"):
        pass
    else:
        connection = sqlite3.connect('Profile.db')  # C������/����������� � ��
        cursor = connection.cursor()  # �������������� ����������� � ��
        createtable()  # C������ ������� � ��
        datainsert(n=15)  # ��������� ������ n ����� ������� � ��
        connection.commit()  # ��������� ���������
        connection.close()  # ��������� ���������� � ��
    result_list = showdbtable()
    return result_list


if __name__ == '__main__':
    main_process()
