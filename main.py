# -*- coding: cp1251 -*-
import os


def main():
    '''Запускает по очереди python модули.
       1)SQLite.py - создает БД, тмблицу в БД, заполняет вводные данные
       2)Selenium.py - парсит ссыли в массив и сохраняет Cookie в БД
       3)Multiprocessing.py - под Cookie из БД заходит по ссылкам из
       массива и обновляет Cookie в БД на новые.
    '''
    folder_path = ""
    script_names = ["SQLite.py", "Selenium.py", "Multiprocessing.py"]
    for script_name in script_names:
        file_path = os.path.join(folder_path, script_name)
        os.system("python " + file_path)


if __name__ == '__main__':
    main()
