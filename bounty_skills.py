import pandas as pd
import matplotlib.pyplot as plt
import squarify

data_skills_top = pd.read_csv('F:\learn_neuro\hhpars\data/data_for_sort.csv')
data_bounty_skills = pd.read_csv('F:\learn_neuro\hhpars\data/data_skills_bounty.csv')

# print(data_skills_top)

# по первой таблице
df = pd.DataFrame()
df['Unnamed: 0'] = data_skills_top['Unnamed: 0']
df['0'] = data_skills_top['2001']

mask = (df['0'] == 0)
print(df)
df = df.loc[df['0'] != 0 ]

print(df)

labels = list(df['Unnamed: 0'])
sizes = list(df['0'])
colors = [plt.cm.Spectral(i/float(len(labels)+0.1)) for i in range(len(labels))]

# Draw Plot
plt.figure(figsize=(120,60), dpi= 80)
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)

# Decorate
plt.title('требования к программисту со знанием Python по 1950 свежих вакансий' )
plt.axis('off')
plt.show()


# # по второй таблице
# df = pd.DataFrame()
# df['Unnamed: 0'] = data_bounty_skills['Unnamed: 0']
# df['0'] = data_bounty_skills['0']
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
# plt.figure(figsize=(35,20), dpi= 80)
# squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)
#
# # Decorate
# plt.title('требования к программисту со знанием Python в топ-10 вакансий')
# plt.axis('off')
# plt.show()