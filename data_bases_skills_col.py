# список скилов делаем

import pandas as pd
import pymorphy3
import functions

data_descriptions = pd.read_csv('F:\learn_neuro\hhpars\data/data_descriptions.csv')
# print(data_descriptions)


# # ручной выбор
# for text in data_descriptions['requirement']:
#     text = functions.text_clean(text)
# data_skills.to_csv('F:\learn_neuro\hhpars\data/data_skills.csv')


# не делаю ранжирование силы требования, какой уровень нужен. пока только хотя бы сами требования собираю. можно
# будет потом брать из самих вакансий окружение
# автовыбор признаков в списки, пока что на базе урезанных дескрипшнов

x = 200

for i in range(x, x+1):
    text, full_list = functions.reparce_for_skills_listlist(data_descriptions, i, vision=1)
    print(text)
    # print(full_list)

# TODO сделать внутри списочков разбор уже по финальным скилам и какое то складирование по подобным

for text_block in full_list:
    if text_block != []:
        print(text_block[0])
