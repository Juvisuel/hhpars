# делаем красивый график кубиками из данных, в первом случае по всей таблице
# во втором случае с выборкой по топ платящих

import pandas as pd
import matplotlib.pyplot as plt
import squarify
import functions

data_vacancies = pd.read_csv('F:\learn_neuro\hhpars\data/data_vacancies1.csv')
data_skills = pd.read_csv('F:\learn_neuro\hhpars\data/data_skills_1.csv')
data_skills = data_skills.drop(['Unnamed: 0.1','Unnamed: 0'], axis=1)


# max_bounty = list(data_vacancies.sort_values('from', ascending=False)['id'])
# list_bounty = []
# for n in range(data_vacancies.shape[0]//100):
#     temp_list = max_bounty[n*100:(n+1)*100]
#     bounty_list = data_vacancies[data_vacancies['id'].isin(temp_list)]
#     mean_bounty = bounty_list.mean()
#     print(mean_bounty)

# print(data_skills_top)

# по первой таблице
# df = pd.DataFrame()
# df['Unnamed: 0'] = data_skills_top['Unnamed: 0']
# df['0'] = data_skills_top['2001']
#
# mask = (df['0'] == 0)
# print(df)
# df = df.loc[df['0'] != 0 ]
#
# print(df)
#
# labels = list(df['Unnamed: 0'])
# sizes = list(df['0'])
# colors = [plt.cm.Spectral(i/float(len(labels)+0.1)) for i in range(len(labels))]
#
# # Draw Plot
# plt.figure(figsize=(120,60), dpi= 80)
# squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)
#
# # Decorate
# plt.title('требования к программисту со знанием Python по 1950 свежих вакансий' )
# plt.axis('off')
# plt.show()




# по второй таблице - циклом (

name = 'питон'

cut = 3  # на сколько частей хотим разделить полученную базу
top = 1   # какую часть из нее хотим смотреть (если top = cut, то все)
percentil = round(100/cut*top)

temp_data_bounty_skills = functions.data_skills_bounty_make(cut,top,data_vacancies,data_skills)
print(temp_data_bounty_skills)

for n in range(0,top):
    df = pd.DataFrame()
    df.index = temp_data_bounty_skills.index
    print(df, n)
    df[n] = temp_data_bounty_skills[n]
    print(df, n)

    df = df.loc[df[n] != 0]

    print(df)

    labels = list(df.index)
    sizes = list(df[n])
    colors = [plt.cm.Spectral(i/float(len(labels)+0.1)) for i in range(len(labels))]

    # Draw Plot
    plt.figure(figsize=(35, 20), dpi=80)
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)

    # Decorate
    plt.title(f'требования в вакансиях топ-{percentil}% {name} ')
    plt.axis('off')
    # plt.savefig(f'F:\learn_neuro\hhpars\data/python_{n}.png')
    plt.show()
