# -*- coding: cp1251 -*-

import random
import time
import json
from Requests import getlinks
from SQLite import incert_cookies_in_db, showdbtable
from selenium import webdriver
from fake_useragent import UserAgent


def add_driver():
    '''Создание обьект драйвер с опциями и юзерагентом.    
       Аргументы: None
       Возвращает: Webdriwer object
    '''
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={useragent.opera}')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path='C:\\Dev2\\ZM_team\\chromedriver\\chromedriver.exe', options=options)
    return driver


def get_cookies() -> None:
    '''Получает Cookies страниц links_list и сохраняет их в БД в STR формате.   
       Аргументы: None
       Возвращает: None
    '''
    links_list = getlinks()
    showdbtable()
    for id in range(15):
        url = random.choice(links_list)  # Выбираем рандомную ссылку c новостью
        db_data = showdbtable()
        if db_data[id][2] is None or db_data[id][2] == []:  # Если cookie не переданы
            try:
                driver = add_driver()
                driver.get(url=url)  # Переходим по выбранной ссылке
                time.sleep(3)
                for i in range(2):  # Прокуручиываем старницу с ранд. задержкой
                    driver.execute_script("window.scrollTo(0, 400);")
                    time.sleep(random.uniform(1, 2))
                cookie = driver.get_cookies()  # Забираем cookie со страницы
                cookie_json = json.dumps(cookie)
                incert_cookies_in_db(cookie_json, id+1)
                driver.close()
                driver.quit()
            except:
                pass
        else:  # Если cookie уже в БД
            print(f'Cookie уже есть в БД для id={id}')
        showdbtable()


if __name__ == '__main__':
    get_cookies()
