

# здесь сравнивается описание вакансии, и если в ней совпали ключевики, то оно плюсуется в таблицу скилов,
# версия для подчитки из сокращенной базы

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import functions
import json
import pandas as pd
from selenium.webdriver.common.by import By

main_url = 'https://api1649064909.delivembd.ws/embed/movie/'
# main_url = 'https://api1649064909.delivembd.ws'
# page = requests.get(main_url)
# soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.title)


dict = {}
for number in range(0, 70000):
    try:
        temp_url = f'{main_url}{number}'
        page = requests.get(temp_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        tit = str(soup.title).replace('<title>','').replace('</title>','')

        dict[tit] = temp_url
        # print(temp_url, tit)
        print(number)

        if number % 100 == 0:
            with open('F:\learn_neuro\hhpars\movie.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(dict, ensure_ascii=False))

    except:pass




