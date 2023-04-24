# -*- coding: cp1251 -*-
import time
import json
from selenium import webdriver
from SQLite import get_cookies_from_db, last_run_update, incert_cookies_in_db
from Requests import getlinks
from fake_useragent import UserAgent
from multiprocessing import Pool

url_list = (getlinks() * 2)[:15]


def open_website_with_cookies(url: str) -> None:
    '''Открывает вебсайты с использованием Cookies.
       Записывает новые Cookies в БД.
       Аргументы: url (str)
       Возвращает: None
    '''
    cookie_list = []
    try:
        useragent = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={useragent.opera}')
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(executable_path='C:\\Dev2\\ZM_team\\chromedriver\\chromedriver.exe', options=options)
        cookie_list = get_cookies_from_db()
        needed_cookies = None
        time.sleep(5)
        driver.get(url=url)
        print('Новостной сайт загрузился без cookies')
        time.sleep(7)
        domain = '.' + driver.current_url.split('/')[2]  # Получаем домен 
        print('Домен открытого сайта =', domain)
        for cookies_dict in cookie_list:
            for value in cookies_dict.values():
                if (domain == value
                    or '.www' + domain == value
                    or 'www' + domain == value
                    or domain[4:] == value
                    or domain[3:] == value
                    or domain[1:] == value):
                    print(f'Домен "{domain}" есть '
                          f'в спсике cookies "{value}"'
                          'словарь с индексом id = '
                          f'{cookie_list.index(cookies_dict)}')
                    needed_cookies = cookie_list[cookie_list
                                                 .index(cookies_dict)]
                    needed_id = cookie_list.index(cookies_dict)
                    needed_domain = domain
                    print('Словарь куки который '
                          'будем использовать:', needed_cookies)
                    last_run_update(id=cookie_list.index(cookies_dict))  # Обновляем счетчик в БД
                    print('Обновились данные в БД в '
                          'строках о количестве использования')
                else:
                    pass
        if needed_cookies is not None:
            print('Пробуем подгрузить Cookies для сайта.')
            driver.add_cookie(cookie_dict=needed_cookies)
            time.sleep(5)
            print('Cookies для сайта успешно подгружены.')
            time.sleep(5)
            driver.refresh()
            print('Страница обновлена со своими Cookies.')
            time.sleep(5)
            new_cookie = driver.get_cookies()  # Забираем новые cookie
            cookie_json = json.dumps(new_cookie)  # Трансформируем
            incert_cookies_in_db(cookie_json, needed_id+1)  # Обновляем БД
            driver.close()
            driver.quit()
            print(f'Попытка для сайта {needed_domain} завершена удачно.')
        else:
            print(f'Cookies для сайта {needed_domain} не нашлись,'
                  'поэтому просто закрываем окно')
            driver.close()
            driver.quit()
            print(f'Попытка для сайта {needed_domain} завершена неудачно.')
    except:
        pass


if __name__ == '__main__':
    p = Pool(processes=5)
    p.map(open_website_with_cookies, url_list)
