# -*- coding: cp1251 -*-
import requests
import time
from bs4 import BeautifulSoup as bs


def getlinks() -> list:
    '''
    Парсит ссылки на новости с сайта 'https://www.news.google.com/home'.
    Аргументы: None
    Возвращает: Список ссылок (list)
    '''
    links_list: list = []
    url = 'https://www.news.google.com/home'
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
            'Safari/537.36',
            'Accept-Language': 'ru-RU'
    }
    response = requests.get(url=url, headers=headers)
    html = bs(response.content, 'lxml')
    time.sleep(2)
    finding_object = html.find_all(class_='WwrzSb')
    for blok in finding_object:
        link_from_html = str(blok).split('href="./')[1].split('" jslog')[0]
        final_news_link = 'https://news.google.com/' + link_from_html
        links_list.append(final_news_link)
    return links_list


if __name__ == '__main__':
    links_list = getlinks()
