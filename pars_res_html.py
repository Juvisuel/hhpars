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

main_url = 'https://api.hh.ru/'



data_vacancies = pd.read_csv(('F:\learn_neuro\hhpars\data/data_vacancies1.csv'))
print(data_vacancies.columns)


# открываем словарь скилов
with open('F:\learn_neuro\hhpars\ dict_skills.txt') as f:
    skills_dict = json.load(f)

# пустой датафрейм для сбора сведений
data_skills = pd.DataFrame(columns=list(skills_dict.values()))
data_skills['id'] = 0
print(data_skills)

for work_page in range(data_vacancies.shape[0]):


    ind = data_vacancies['id'][work_page]
    temp_url = data_vacancies.alternate_url[work_page]
    print(temp_url)


    # здесь слистываем HH, обычным реквестом не вышло
    driver = webdriver.Chrome('F:\learn_neuro\hhpars\driver/chromedriver.exe')
    driver.get(temp_url)
    time.sleep(2)
    page = driver.page_source
    assert "No results found." not in driver.page_source
    driver.close()
    #
    soup = BeautifulSoup(page, 'html.parser')
    text = soup.find('div', class_='vacancy-branded-user-content')
    print(text)

    if text:


        # сюда подается текст вакансии и его индекс он внутри проверяется на скилы и отмечаются совпадения.
        # Возвращается срока БД с отметками синхронно столбцам бошльшой таблицы скилов.
        skill_list = functions.match_vacancy_skills_to_skill_list(str(text), skills_dict, ind,vision=0)
        data_skills.loc[ind] = skill_list

#смотрим готовую таблицу скилов
print(data_skills)

data_skills.to_csv('F:\learn_neuro\hhpars\data/data_skills_2.csv')