import requests
import pprint
import pandas as pd
import functions

main_url = 'https://api.hh.ru/'


# specialisations = requests.get(main_url+'specializations')
# pprint.pprint(specialisations.json())


# VACANCIES

# list_columns = ['id', 'description', 'key_skills', 'schedule',
#                 'accept_handicapped', 'accept_kids',
#                 'experience', 'address',
#                 'alternate_url', 'apply_alternate_url', 'employment','salary',
#                 'salary.from', 'salary.to', 'salary.gross', 'salary.currency',
#                 'archived', 'name', 'area', 'area.id', 'area.name', 'created_at','published_at',
#                 'employer', 'type', 'specialization', 'specializations[].name', 'driver_license_types',
#                 'driver_license_types[].id', 'working_days', 'working_time_intervals',
#                 'working_time_modes','accept_temporary','professional_roles']

main_url = 'https://api.hh.ru/'
position = 'python'
count = 1999
data_vacancies = functions.data_vacancies(main_url, position, count)


# вывод с сортировкой по окладу "от"
# print(data_vacancies.sort_values('from', ascending=False))

data_descriptions, data_vacancies1 = functions.id_expanse(main_url, data_vacancies)

print(data_vacancies1)
print(data_descriptions)

data_descriptions.to_csv('F:\learn_neuro\hhpars\data/data_descriptions.csv')
data_vacancies1.to_csv('F:\learn_neuro\hhpars\data/data_vacancies1.csv')
