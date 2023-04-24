# -*- coding: cp1251 -*-
import os


def main():
    '''��������� �� ������� python ������.
       1)SQLite.py - ������� ��, ������� � ��, ��������� ������� ������
       2)Selenium.py - ������ ����� � ������ � ��������� Cookie � ��
       3)Multiprocessing.py - ��� Cookie �� �� ������� �� ������� ��
       ������� � ��������� Cookie � �� �� �����.
    '''
    folder_path = ""
    script_names = ["SQLite.py", "Selenium.py", "Multiprocessing.py"]
    for script_name in script_names:
        file_path = os.path.join(folder_path, script_name)
        os.system("python " + file_path)


if __name__ == '__main__':
    main()
