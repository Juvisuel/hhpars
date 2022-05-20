import requests
import pprint
import pandas as pd


# генерится порядковый номер страницы
def generate_str_request(name, text, page):

    name_str = name+'vacancies?&page='+str(page)+'&text='+text
    return name_str


# вакансия разбирается по значимым столбцам таблицы, функция. цикл берется из списка,
# не совпадающего со столбцами таблицы, так как для двух из них мы берем только один из параметров
# следующего уровня словаря

def parse_id(data_json_object, temp_data, data_items):

    loc_number = temp_data.shape[0]
    temp_data.loc[loc_number] = 0

    for item in data_items:
        for key, value in data_json_object.items():

            if key == item:
                if key == 'snippet':
                    for key1, value1 in value.items():
                        temp_data.loc[loc_number, key1] = str(value1).replace(
                            '<highlighttext>', '').replace('</highlighttext>', '')

                # забирается только "от"
                elif key == 'salary':
                    if type(value) == dict:
                        salary = list(value.values())
                        temp_data.loc[loc_number, 'from'] = salary[0]
                    else:
                        temp_data.loc[loc_number, 'from'] = 0

                elif key in temp_data.columns:
                    temp_data.loc[loc_number, key] = str(value).replace('<highlighttext>', '')

    return temp_data

# разбираем json в таблицу


def data_vacancies(main_url, position, count):

    data_items = ['name', 'snippet', 'id', 'alternate_url', 'area',
                          'responsibility', 'salary', 'from', 'requirement', 'description']

    list_columns_ultrashort = ['name', 'id', 'alternate_url',  'area',
                               'responsibility', 'from', 'requirement', 'description']

    data_vacancies1 = pd.DataFrame(columns=list_columns_ultrashort)

    for page in range(count//20):
        print(page)
        temp_url = generate_str_request(main_url, position, page)
        # print(temp_url)
        vacancies = requests.get(temp_url)

        for local_result in vacancies.json()['items']:
            data_vacancies1 = parse_id(local_result, data_vacancies1, data_items)

    return data_vacancies1


# тащим по ID подробное описание и добавляем


def id_expanse(main_url, data_vacancies2):

    temp_data = pd.DataFrame(columns=['id', 'descriptions', 'requirement'])
    for x in data_vacancies2.index:
        temp_id = data_vacancies2.loc[x, 'id']
        try:
            text = requests.get(main_url + 'vacancies/'+temp_id).json()['description']
            text = text.replace('<p>', '').replace('</p>', '').replace('<ul>', '').replace('<li>', '').replace(
                '</strong>', '').replace('<strong>', '').replace('<br', '').replace('<em>', '').replace(
                '/>', '').replace('</li>', '').replace('ul>', '').replace('<', '').replace(':', '').replace(';', '')
            temp_data.loc[x] = [temp_id, text, str(data_vacancies2.loc[x, 'requirement'])]
            data_vacancies2.loc[x, 'descriptions'] = text
        except:
            pass

    return temp_data, data_vacancies2
