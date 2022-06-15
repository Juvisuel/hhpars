import pandas as pd
import functions

main_url = 'https://api.hh.ru/'
position = 'python'

count = 1999

data_vacancies = functions.data_vacancies(main_url, position, count)
data_descriptions, data_vacancies1 = functions.id_expanse(main_url, data_vacancies)

