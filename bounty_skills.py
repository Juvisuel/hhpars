import pandas as pd
import matplotlib.pyplot as plt
import squarify

data_skills_top = pd.read_csv('F:\learn_neuro\hhpars\data/data_for_sort.csv')
data_bounty_skills = pd.read_csv('F:\learn_neuro\hhpars\data/data_skills_bounty.csv')
data_vacancies = pd.read_csv('F:\learn_neuro\hhpars\data/data_vacancies1.csv')
max_bounty = list(data_vacancies.sort_values('from', ascending=False)['id'])

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




# по второй таблице
df = pd.DataFrame()
df['Unnamed: 0'] = data_bounty_skills['Unnamed: 0']

for n in range(9):
    df = pd.DataFrame()
    df['Unnamed: 0'] = data_bounty_skills['Unnamed: 0']
    df[str(n)] = data_bounty_skills[str(n)]

    df = df.loc[df[str(n)] != 0 ]

    print(df)

    labels = list(df['Unnamed: 0'])
    sizes = list(df[str(n)])
    colors = [plt.cm.Spectral(i/float(len(labels)+0.1)) for i in range(len(labels))]

    # Draw Plot
    plt.figure(figsize=(35,20), dpi= 80)
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)


    # Decorate
    plt.title(f'требования к программисту со знанием Python в вакансиях {n} ')
    plt.axis('off')
    plt.savefig(f'F:\learn_neuro\hhpars\data/python_{n}.png')
    # plt.show()