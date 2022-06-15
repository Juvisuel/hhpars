# список скилов делаем, на выходе словарь. todo сделать хэширование уже здесь как-то может токенизацией чтоб ключи ок?

import pandas as pd
import pymorphy3
import functions
import json

data_descriptions = pd.read_csv('F:\learn_neuro\hhpars\data/data_descriptions.csv')
# print(data_descriptions)


# # ручной выбор
# for text in data_descriptions['requirement']:
#     text = functions.text_clean(text)
# data_skills.to_csv('F:\learn_neuro\hhpars\data/data_skills.csv')


# не делаю ранжирование силы требования, какой уровень нужен. пока только хотя бы сами требования собираю. можно
# будет потом брать из самих вакансий окружение
# автовыбор признаков в списки, пока что на базе урезанных дескрипшнов
def auto_ident_skills(data_descriptions):
    level_0 = {}

    for i in range(data_descriptions.shape[0]):
        if i%100 == 0:
            print(f'{i} из {data_descriptions.shape[0]}')

        text, full_list = functions.reparce_for_skills_listlist_zero(data_descriptions[i, 'requirement'], vision=0)

        for text_block in full_list:
            if text_block != []:
                for skills in text_block:
                    if skills != []:
                        for skill in skills:
                            if skill.lower() not in level_0.values():
                                level_0[len(level_0.items())] = skill.lower()

    return level_0

level_0_dict = auto_ident_skills(data_descriptions)

with open('data/dict_skills.txt', 'w') as temp_file:
    json.dump(level_0_dict, temp_file)



