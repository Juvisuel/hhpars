# здесь сравнивается описание вакансии, и если в ней совпали ключевики, то оно плюсуется в таблицу скилов

import pandas as pd
import pymorphy3

import functions

data_descriptions = pd.read_csv('F:\learn_neuro\hhpars\data/data_descriptions.csv')
data_skills = pd.read_csv('F:\learn_neuro\hhpars\data/data_skills.csv')
data_skills['id'] = 0



morph = pymorphy3.MorphAnalyzer()



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


for i in data_descriptions.index:

    skill_rate_temp = pd.DataFrame(columns=data_skills.columns)
    text = data_descriptions.loc[i, 'requirement']
    text2 = data_descriptions.loc[i, 'descriptions']
    ind = data_descriptions.loc[i, 'id']
    # print(ind)
    skill_rate_temp.loc[ind] = 0
    text += text2

    # text = functions.encodeTextRazmetka()

    text = text.replace('.', '').replace('/', ' ').replace('?', ' ').replace(
        ',', ' ').replace('(', ' ').replace(')', ' ')
    text = text.split()

    for string_data in text:
        name = str(string_data).lower()
        try:
            name = morph.normal_forms(name)
            name = str(name[0])
            # print(name)
        except:
            name = str(name)
        for j, column in enumerate(skill_rate_temp.columns):
            if name == column:
                skill_rate_temp[column] += 1

    skill_rate_temp['id'] = ind
    skill_list = list(skill_rate_temp.loc[ind])

    data_skills.loc[i] = skill_rate_temp.loc[ind]

print(data_skills)

data_skills.to_csv('F:\learn_neuro\hhpars\data/data_skills_1.csv')
