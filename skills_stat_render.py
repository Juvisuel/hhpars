# здесь сравнивается описание вакансии, и если в ней совпали ключевики, то оно плюсуется в таблицу скилов,
# версия для подчитки из сокращенной базы

import pandas as pd
import json

import functions

data_descriptions = pd.read_csv('F:\learn_neuro\hhpars\data/data_descriptions.csv')

# здесь таблица от ручного разбора
# data_skills = pd.read_csv('F:\learn_neuro\hhpars\data/data_skills.csv')
# data_skills['id'] = 0
# print(data_skills)


# здесь таблица от неручного
with open('F:\learn_neuro\hhpars\ dict_skills.txt') as f:
    skills_dict = json.load(f)
data_skills = pd.DataFrame(columns=list(skills_dict.values()))
data_skills['id'] = 0
print(data_skills)

# for i in data_descriptions.index:
#
#     skill_rate_temp = pd.DataFrame(columns=data_skills.columns)
#     text = data_descriptions.loc[i, 'requirement']
#     text2 = data_descriptions.loc[i, 'descriptions']
#     ind = data_descriptions.loc[i, 'id']
#     # print(ind)
#     skill_rate_temp.loc[ind] = 0
#     text += text2
#
#     text = text.replace('.', '').replace('/', ' ').replace('?', ' ').replace(
#         ',', ' ').replace('(', ' ').replace(')', ' ')
#     text = text.split()
#
#     for string_data in text:
#         name = str(string_data).lower()
#         try:
#             name = morph.normal_forms(name)
#             name = str(name[0])
#             # print(name)
#         except:
#             name = str(name)
#         for j, column in enumerate(skill_rate_temp.columns):
#             if name == column:
#                 skill_rate_temp[column] += 1
#
#     skill_rate_temp['id'] = ind
#     skill_list = list(skill_rate_temp.loc[ind])
#
#     data_skills.loc[i] = skill_rate_temp.loc[ind]
#
# print(data_skills)
#
# data_skills.to_csv('F:\learn_neuro\hhpars\data/data_skills_1.csv')
#
test_number = 1980

for ind, i in enumerate(data_descriptions.index):

    while ind < test_number:

        if ind%10 == 0:
            print(f'{i} из {data_descriptions.shape[0]}')

        skill_rate_temp = pd.DataFrame(columns=data_skills.columns)
        text = data_descriptions.loc[i, 'requirement']
        text2 = data_descriptions.loc[i, 'descriptions']
        ind = data_descriptions.loc[i, 'id']
        # print(ind)
        skill_rate_temp.loc[ind] = 0
        text += text2

        # складываем скилы в базу
        # получаем распарсенное на кусочки описание вакансии
        skills, full_list = functions.reparce_for_skills_listlist_zero(text, vision=0)


        # здесь плюсуем найденные скилы

        for text_block in full_list:
            if text_block != []:
                for skills in text_block:
                    if skills != []:
                        for skill in skills:
                            if skill.lower() in skills_dict.values():
                                for j, column in enumerate(skill_rate_temp.columns):
                                    if skill == column:
                                            skill_rate_temp[column] += 1

        skill_rate_temp['id'] = ind
        skill_list = list(skill_rate_temp.loc[ind])


        data_skills.loc[ind] = skill_list


print(data_skills)

data_skills.to_csv('F:\learn_neuro\hhpars\data/data_skills_1.csv')
