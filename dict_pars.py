
from bs4 import BeautifulSoup
import requests
import functions
import json
import pandas as pd
from selenium.webdriver.common.by import By
from tokenizer import tokenizer_from_json
main_url = 'https://kartaslov.ru/'








#они#Значение

with open('f:/FTP_Work/hirokama/Translator/accos/tokenizer.json') as f:
    data_translator = json.load(f)
    tokenizer = tokenizer_from_json(data_translator)
with open('F:/learn_neuro/redactor_text/tokenizer/tokenizer_2.json') as f:
    data_translator = json.load(f)
    tokenizer2 = tokenizer_from_json(data_translator)


list_new_words = range(10000,10001)
list_unknown = []
for number in list_new_words:
    word = tokenizer2.sequences_to_texts([[number]])[0]
    try:
        print(word)
        temp_url = f'{main_url}/значение-слова/{word}'
        page = requests.get(temp_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # moduleansver = soup.body.descendants
        module_ansver = soup.find('div', class_="container")
        module2 = module_ansver.find('div', class_='col-6 col-lg-4 v2-margins')
        print(soup.find_all('b'))

        # module4 = module3.find('li', class_='v2-dict-entry-text')
        # module_ansver = soup.find('span', id="Значение")


        # for item in module_ansver:
        #     print(item)


        # tit = str(soup.title).replace('<title>','').replace('</title>','')

        # dict[word] = text
        # print(temp_url, tit)
        print(number)
        #
        # if number % 100 == 0:
        #     with open('F:\learn_neuro\hhpars\movie.json', 'w', encoding='utf-8') as f:
        #         f.write(json.dumps(dict, ensure_ascii=False))



    except:
        list_unknown.append(word)
        pass

print(list_unknown)