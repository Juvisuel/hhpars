import pandas as pd

data_skills = pd.read_csv('F:\learn_neuro\hhpars\data/data_skills_1.csv')
data_skills = data_skills.drop(['Unnamed: 0.1','Unnamed: 0'], axis=1)
data_vacancies = pd.read_csv(('F:\learn_neuro\hhpars\data/data_vacancies1.csv'))

print(data_skills)

summ = []
for column in data_skills.columns:
   summ.append(data_skills[column].sum())

data_skills.loc['2001'] = summ


data_for_sort = data_skills.drop('id',axis=1).transpose()
data_for_sort = data_for_sort.sort_values('2001', ascending=False)

data_for_sort.to_csv('F:\learn_neuro\hhpars\data/data_for_sort.csv')

max_bounty = list(data_vacancies.sort_values('from', ascending=False)['id'])
# print(max_bounty)

data_skills_bounty = pd.DataFrame(columns=data_skills.columns)

for count in range(data_vacancies.shape[0]//100):
   companies = max_bounty[int(count*100):int((count+1)*100)]
   # print(companies)
   temp_skills = data_skills[data_skills['id'].isin(companies)] ######
   # print(temp_skills)
   summ = []
   for column in data_skills.columns:
      summ.append(temp_skills[column].sum())
   data_skills_bounty.loc[count] = summ

data_skills_bounty = data_skills_bounty.drop('id', axis = 1)
data_skills_bounty = data_skills_bounty.transpose()
print(data_skills_bounty)

data_skills_bounty.to_csv('F:\learn_neuro\hhpars\data/data_skills_bounty.csv')