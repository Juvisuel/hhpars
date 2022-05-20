import pandas as pd
import pymorphy3

data_descriptions = pd.read_csv('F:\learn_neuro\hhpars\data/data_descriptions.csv')
# print(data_descriptions)

data_skills = pd.DataFrame()
morph = pymorphy3.MorphAnalyzer()

print(morph.normal_forms('близко'))

for text in data_descriptions['requirement']:

    text = text.replace('.', '').replace('/', ' ').replace('?', ' ').replace(
        ',', ' ').replace('(', ' ').replace(')', ' ')
    text = text.split()

    for string_data in text:
        choice = int(input(f' {string_data}   1 = да , 0 = нет, 3 = прекратить работу '))
        name = str(string_data).lower()
        try:
            name = morph.normal_forms(name)
            name = str(name[0])
            print(name)
        except:
            name = str(name)
        if choice == 1:

            if name not in data_skills.columns:
                data_skills[name] = 0
            else:
                print('этот скил уже есть')


        elif choice == 3:
            print(data_skills)

            break

        # data_skills.to_csv('F:\learn_neuro\hhpars\data/data_skills.csv')

