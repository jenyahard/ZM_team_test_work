# -*- coding: cp1251 -*-

import random
import time
import json
from Requests import getlinks
from SQLite import incert_cookies_in_db, showdbtable
from selenium import webdriver
from fake_useragent import UserAgent


def add_driver():
    '''�������� ������ ������� � ������� � �����������.    
       ���������: None
       ����������: Webdriwer object
    '''
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={useragent.opera}')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path='C:\\Dev2\\ZM_team\\chromedriver\\chromedriver.exe', options=options)
    return driver


def get_cookies() -> None:
    '''�������� Cookies ������� links_list � ��������� �� � �� � STR �������.   
       ���������: None
       ����������: None
    '''
    links_list = getlinks()
    showdbtable()
    for id in range(15):
        url = random.choice(links_list)  # �������� ��������� ������ c ��������
        db_data = showdbtable()
        if db_data[id][2] is None or db_data[id][2] == []:  # ���� cookie �� ��������
            try:
                driver = add_driver()
                driver.get(url=url)  # ��������� �� ��������� ������
                time.sleep(3)
                for i in range(2):  # �������������� �������� � ����. ���������
                    driver.execute_script("window.scrollTo(0, 400);")
                    time.sleep(random.uniform(1, 2))
                cookie = driver.get_cookies()  # �������� cookie �� ��������
                cookie_json = json.dumps(cookie)
                incert_cookies_in_db(cookie_json, id+1)
                driver.close()
                driver.quit()
            except:
                pass
        else:  # ���� cookie ��� � ��
            print(f'Cookie ��� ���� � �� ��� id={id}')
        showdbtable()


if __name__ == '__main__':
    get_cookies()
