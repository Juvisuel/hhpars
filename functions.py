import requests
import pprint
import pandas as pd
import pymorphy3


# генерится порядковый номер страницы
def generate_str_request(name, text, page):
    name_str = name + 'vacancies?&page=' + str(page) + '&text=' + text
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

    list_columns_ultrashort = ['name', 'id', 'alternate_url', 'area',
                               'responsibility', 'from', 'requirement', 'description']

    data_vacancies1 = pd.DataFrame(columns=list_columns_ultrashort)

    for page in range(count // 20):
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
            text = requests.get(main_url + 'vacancies/' + temp_id).json()['description']
            text = text.replace('<p>', '').replace('</p>', '').replace('<ul>', '').replace('<li>', '').replace(
                '</strong>', '').replace('<strong>', '').replace('<br', '').replace('<em>', '').replace(
                '/>', '').replace('</li>', '').replace('ul>', '').replace('<', '').replace(':', '').replace(';', '')
            temp_data.loc[x] = [temp_id, text, str(data_vacancies2.loc[x, 'requirement'])]
            data_vacancies2.loc[x, 'descriptions'] = text
        except:
            pass

    return temp_data, data_vacancies2


#  ФУНКЦИЯ, КОТОРАЯ ВЕРНЕТ ТАБЛИЦУ С СУММАМИ ПО СКИЛАМ, ДЛЯ ГРАФИКА
def data_skills_bounty_make(cut, top, data_vacancies, data_skills):
    data_skills_bounty = pd.DataFrame(columns=data_skills.columns)
    if top <= cut:

        # cut = 10  # на сколько частей хотим разделить полученную базу
        # top = 1   # какую часть из нее хотим смотреть (если top = cut, то все)

        max_bounty = list(data_vacancies.sort_values('from', ascending=False)['id'])
        cutter = data_vacancies.shape[0] // cut
        range_number = data_vacancies.shape[0] // cutter
        # print(cutter,range_number)

        for count in range(top):

            companies = max_bounty[int(count * cutter):int((count + 1) * cutter)]
            # print(companies)
            temp_skills = data_skills[data_skills['id'].isin(companies)]  ######
            # print(temp_skills)
            summ = []
            for column in data_skills.columns:
                summ.append(temp_skills[column].sum())
            data_skills_bounty.loc[count] = summ

        data_skills_bounty = data_skills_bounty.drop('id', axis=1)
        data_skills_bounty = data_skills_bounty.transpose()

    else:
        raise
        print('выберите часть маньше целого')
        # print(data_skills_bounty)
    return (data_skills_bounty)


# простая чистка сырого текста
def text_clean(text1):
    text2 = text1.replace('.', '').replace('/', ' ').replace('?', ' ').replace(
        ',', ' ').replace('(', ' ').replace(')', ' ')
    text2 = text2.split()
    return text2


# c ручным выбором
def table_skills(text):
    data_skills = pd.DataFrame()
    morph = pymorphy3.MorphAnalyzer()
    choice = 0
    while choice < 3:
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

    return data_skills


# текст в список списков с разделителями для автовыбора
def encodeTextRazmetka(text):
    textBlock = []
    textList = []
    textNumber = []

    textBase = pd.DataFrame()
    n = 0
    word = ''
    status = ''
    morph = pymorphy3.MorphAnalyzer()
    except_list = ['деньги', 'очки']

    for index, i in enumerate(text):

        if i == '/' or i == '?' or i == '.' or i == ';' or i == ':' or index == len(text) - 1 or i == '—':
            if index == len(text) - 1 and i != '?' and i != '/' and i != '.' and i != ';' and i != ':':
                word = str(word) + i

            if len(word) > 0:
                rawWord = word
                p = morph.parse(word)[0]
                if p.tag.POS == 'NOUN':  # дописать что это местоимение
                    if p.tag.case == 'nomn':
                        status = 'hero'
                        # print('герой', word)
                    if p.tag.case != 'nomn':
                        # print('объект', word)
                        status = 'obj'
                if p.tag.POS == 'VERB':
                    # print('действие', word)
                    status = 'deal'
                if p.tag.POS == 'ADJF':
                    if p.tag.case == 'nomn':
                        # print('признак героя', word)
                        status = 'adjhero'
                    if p.tag.case != 'nomn':
                        # print('признак объекта', word)
                        status = 'adjobj'

                if word not in except_list:
                    word = morph.parse(word)[0].normal_form

                temp = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord]
                list_temp = pd.DataFrame()
                list_temp[n] = temp

                textBase = pd.concat([textBase, list_temp], axis=1)

                status = ''

                textBlock.append(word)
                textNumber.append(n)

                n = n + 1
                word = ''

            textList.append(textBlock)
            textBlock = []



        elif i == ' ' or i == ',' or i == '"' or i == '(' or i == ')' or i == '\ '[0]:
            if len(word) > 0:
                rawWord = word
                # герой и действие
                p = morph.parse(word)[0]
                if p.tag.POS == 'NOUN' or p.tag.POS == 'NPRO':
                    if p.tag.case == 'nomn':
                        status = 'hero'
                        # print('герой', word)
                    if p.tag.case != 'nomn':
                        # print('объект', word)
                        status = 'obj'
                if p.tag.POS == 'VERB':
                    # print('действие', word)
                    status = 'deal'
                if p.tag.POS == 'ADJF':
                    if p.tag.case == 'nomn':
                        # print('признак героя', word)
                        status = 'adjhero'
                    if p.tag.case != 'nomn':
                        # print('признак объекта', word)
                        status = 'adjobj'
                if p.tag.POS == 'ADVB':
                    # print('признак действия', word)
                    status = 'adjdeal'

                # норм форм
                if word not in except_list:
                    word = morph.parse(word)[0].normal_form

                temp = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord]
                list_temp = pd.DataFrame()
                list_temp[n] = temp

                textBase = pd.concat([textBase, list_temp], axis=1)
                status = ''

                textBlock.append(word)
                textNumber.append(n)

                n = n + 1
                word = ''

        else:  # тут наверное можно дать ей сразу списком знаки
            word = str(word) + i

    # print(n)
    # print(textList)

    return textList, textBase


def check_word(word):
    # исключения нужны для убирания мусорных частей речи и слов

    except_list = ['PREP', 'NPRO', 'CONJ', 'INFN', 'PRTS', 'GRND', 'PRTF', 'NUMR', 'PRCL', 'INTJ', 'ADVB', 'PRED']
    except_list1 = [
        'опыт', 'знание', 'понимание', 'работа', 'год', '3‐х', 'х', 'умение', 'владение',
        'сложный', 'запрос', 'больший', ' ', 'использование', 'должный', 'естественный', 'хороший',
        'новый', 'большой', 'плюс', 'любой', 'команда', 'обучение', 'знакомство', 'связанный', 'часть',
        'способность', 'желание', 'такой', 'связанный', 'желательный', 'помощь',
        'развитие', 'митап', 'встреча', 'сам', 'отличный', 'преимущество', 'базовый', 'который',
        'митап', 'тема', 'обмен', 'актуальный', 'внутренний', 'архитектурный', 'возможность',
        'профессиональный', 'полный', 'частичный', 'практика', 'документация', 'чтение', 'достаточный',
        'тот', 'этот', 'уровень', 'библиотека', 'наличие', 'проект', 'background',
        'обертка', 'встраивание', 'обернуть', 'встроить', 'обёртка', 'написание', 'подход', 'последующая',
        'миграция', 'отдельный', 'компания', 'разработчик', 'иной', 'другой', 'качественный', 'практический',
        'поддержание', 'уверенный', 'конкурентный', 'семейство', 'свой',
        'код', 'высокий', 'принцип', 'особенность', 'построение', 'портфолио', 'упорство', 'продуктивность', '3х'
    ]
    if not str(word[0]).isdigit() and word[0] not in except_list1 and word[1] not in except_list:
        return True


# разбор текста на блоки скилов

def reparce_for_skills(data, temp_index):
    text = data.loc[temp_index, 'requirement']
    text1, text_base = encodeTextRazmetka(text)

    full_list = []
    list_local_obj = []
    list_local_hero = []
    for i in text_base.columns:

        path = text_base[i]

        if check_word(path):
            # print(path)
            if path[3] == 'hero':
                list_local_hero.append(path[5])
                path[3] = None

                for j in text_base.columns:
                    path_adj = text_base[j]

                    if check_word(path_adj):
                        if path_adj[3] == 'adjhero':
                            list_local_hero.insert(0, path_adj[5])
                            text_base[j][3] = None

            if text_base[i][3] == 'obj' or text_base[i][3] == '':
                list_local_obj.append(text_base[i][5])
                text_base[i][3] = None

                in_point = i - 3 if i >= 3 else 0
                out_point = i + 3 if i <= text_base.shape[1] - 3 else text_base.shape[1]

                for j in text_base.columns[in_point:out_point]:
                    path_adj = text_base[j]
                    if check_word(path_adj):

                        if text_base[j][3] == 'adjobj':

                            if j > i:
                                list_local_obj.append(text_base[j][5])
                            else:
                                list_local_obj.insert(len(list_local_obj) - 1, text_base[j][5])
                            text_base[j][3] = None

    # второй круг, спец для случая если система перепутала признак объекта и субьекта,
    # проходим по базе, в которой уже сняты метки

    # print(text)
    # print(list_local_obj, list_local_hero)
    for i in text_base.columns:
        if check_word(text_base[i]):
            if text_base[i][3] == 'adjobj' or text_base[i][3] == 'adjhero':
                list_local_obj.append(text_base[i][5])
                text_base[i][3] = None

    # print(list_local_hero + list_local_obj)
    return list_local_hero + list_local_obj


# разбор текста на блоки скилов, но с листами листов, проверяет отдельно объекты отдельно субьекты, учитывает
# разные предложения
def reparce_for_skills_listlist(data, temp_index, vision):
    text = data.loc[temp_index, 'requirement']
    text1, temp_base = encodeTextRazmetka(text)

    gigant_list = []

    # режем базу по предложениям

    for cutter in range(temp_base.loc[4].max() + 1):
        columns_for_drop = [x for x in temp_base.columns if temp_base[x][4] != cutter]
        text_base = temp_base.drop(columns=columns_for_drop, axis=0)

        if vision:
            print(text_base)

        full_list = []
        temp_word = ['temp', 0]
        list_local_obj = []
        list_local_hero = []

        # для каждого предложения отдельно

        for i in text_base.columns:

            path = text_base[i]
            if path[4] > temp_word[1] and list_local_obj:

                if list_local_obj not in full_list and list_local_obj != []:
                    full_list.append(list_local_obj)
                if list_local_hero not in full_list and list_local_hero != []:
                    full_list.append(list_local_hero)

                list_local_obj = []
                list_local_hero = []

            if vision:
                print(temp_word)

            # проверка героев (их обычно один на предложение, и все признаки их)
            if check_word(path):
                if vision:
                    print(path)
                if path[3] == 'hero':
                    if vision:
                        print('герой', path[5])
                    list_local_hero = [path[5]]
                    path[3] = None
                    temp_word = ['hero', path[4]]

                    for j in text_base.columns:
                        path_adj = text_base[j]

                        if check_word(path_adj) and path_adj[4] == path[4]:

                            if path_adj[3] == 'adjhero':
                                if vision:
                                    print('признак героя ', path_adj[5])
                                list_local_hero.insert(0, path_adj[5])
                                path_adj[3] = None
                                temp_word = ['adjhero', path[4]]

                    full_list.append(list_local_hero)

                # проверка объектов (их обычно несколько)
                if path[3] == 'obj' or path[3] == '':
                    # проверка не являются ли объекты одним описанием

                    if temp_word[0] == 'obj' or temp_word[0] == 'adjobj' and temp_word[1] == path[4]:
                        if vision:
                            print('объекты одного блока, добавляем', path[5])
                            print(list_local_obj)
                        list_local_obj.append(path[5])
                        # print(list_local_obj)

                    elif temp_word[0] == 'hero' or temp_word[0] == 'adjhero' and temp_word[1] == path[4]:
                        list_local_hero.append(path[5])
                        if vision:
                            print('возможно группа героя', path[5])
                            print(list_local_hero)


                    else:
                        if vision:
                            print('заново', path[5])
                        list_local_obj = [path[5]]

                    path[3] = None

                    # добавка признаков

                    in_point = i - 3 if i >= 3 else 0
                    out_point = i + 3 if i <= text_base.shape[1] - 3 else text_base.shape[1]

                    if vision:
                        print('обьект', path[5])
                        print(in_point, out_point)
                        print('смотрим признаки')

                    temp_word = ['obj', path[4]]

                    for j in text_base.columns[in_point:out_point]:
                        path_adj = text_base[j]

                        if check_word(path_adj):

                            if path_adj[3] == 'adjobj':
                                if vision:
                                    print('признак объекта', path_adj[5])

                                if j > i:
                                    list_local_obj.append(path_adj[5])
                                else:
                                    list_local_obj.insert(len(list_local_obj) - 1, path_adj[5])
                                path_adj[3] = None
                                temp_word = ['adjobj', path[4]]

                            elif path_adj[3] == 'hero' or path_adj[3] == 'adjhero' and temp_word[1] == path_adj[4]:
                                if j > i:
                                    list_local_hero.append(path_adj[5])
                                else:
                                    list_local_hero.insert(len(list_local_obj) - 1, path_adj[5])

                    if list_local_obj not in full_list and list_local_obj != []:
                        full_list.append(list_local_obj)
                    if list_local_hero not in full_list and list_local_hero != []:
                        full_list.append(list_local_hero)

                elif path[3] == 'adjobj':
                    temp_word = ['adjobj', path[4]]
                elif path[3] == 'adjhero':
                    temp_word = ['adjhero', path[4]]

        # второй круг, спец для случая если система перепутала признак объекта и субьекта,
        # проходим по базе, в которой уже сняты метки

        # # print(text)
        # # print(list_local_obj, list_local_hero)
        # for i in text_base.columns:
        #     if check_word(text_base[i]):
        #         if text_base[i][3] == 'adjobj' or text_base[i][3] == 'adjhero':
        #             full_list.append([text_base[i][5]])
        #             text_base[i][3] = None

        gigant_list.append(full_list)

    # print(list_local_hero + list_local_obj)

    return text, gigant_list


# версия которая отдает начальную форму
def reparce_for_skills_listlist_zero(text, vision):
    text1, temp_base = encodeTextRazmetka(text)

    gigant_list = []

    # режем базу по предложениям

    for cutter in range(temp_base.loc[4].max() + 1):
        columns_for_drop = [x for x in temp_base.columns if temp_base[x][4] != cutter]
        text_base = temp_base.drop(columns=columns_for_drop, axis=0)

        if vision:
            print(text_base)

        full_list = []
        temp_word = ['temp', 0]
        list_local_obj = []
        list_local_hero = []

        # для каждого предложения отдельно

        for i in text_base.columns:

            path = text_base[i]
            if path[4] > temp_word[1] and list_local_obj:

                if list_local_obj not in full_list and list_local_obj != []:
                    full_list.append(list_local_obj)
                if list_local_hero not in full_list and list_local_hero != []:
                    full_list.append(list_local_hero)

                list_local_obj = []
                list_local_hero = []

            if vision:
                print(temp_word)

            # проверка героев (их обычно один на предложение, и все признаки их)
            if check_word(path):
                if vision:
                    print(path)
                if path[3] == 'hero':
                    if vision:
                        print('герой', path[0])
                    list_local_hero = [path[0]]
                    path[3] = None
                    temp_word = ['hero', path[4]]

                    for j in text_base.columns:
                        path_adj = text_base[j]

                        if check_word(path_adj) and path_adj[4] == path[4]:

                            if path_adj[3] == 'adjhero':
                                if vision:
                                    print('признак героя ', path_adj[0])
                                list_local_hero.insert(0, path_adj[0])
                                path_adj[3] = None
                                temp_word = ['adjhero', path[4]]

                    full_list.append(list_local_hero)

                # проверка объектов (их обычно несколько)
                if path[3] == 'obj' or path[3] == '':
                    # проверка не являются ли объекты одним описанием

                    if temp_word[0] == 'obj' or temp_word[0] == 'adjobj' and temp_word[1] == path[4]:
                        if vision:
                            print('объекты одного блока, добавляем', path[0])
                            print(list_local_obj)
                        list_local_obj.append(path[0])
                        # print(list_local_obj)

                    elif temp_word[0] == 'hero' or temp_word[0] == 'adjhero' and temp_word[1] == path[4]:
                        list_local_hero.append(path[0])
                        if vision:
                            print('возможно группа героя', path[0])
                            print(list_local_hero)


                    else:
                        if vision:
                            print('заново', path[0])
                        list_local_obj = [path[0]]

                    path[3] = None

                    # добавка признаков

                    in_point = i - 3 if i >= 3 else 0
                    out_point = i + 3 if i <= text_base.shape[1] - 3 else text_base.shape[1]

                    if vision:
                        print('обьект', path[0])
                        print(in_point, out_point)
                        print('смотрим признаки')

                    temp_word = ['obj', path[4]]

                    for j in text_base.columns[in_point:out_point]:
                        path_adj = text_base[j]

                        if check_word(path_adj):

                            if path_adj[3] == 'adjobj':
                                if vision:
                                    print('признак объекта', path_adj[0])

                                if j > i:
                                    list_local_obj.append(path_adj[0])
                                else:
                                    list_local_obj.insert(len(list_local_obj) - 1, path_adj[0])
                                path_adj[3] = None
                                temp_word = ['adjobj', path[4]]

                            elif path_adj[3] == 'hero' or path_adj[3] == 'adjhero' and temp_word[1] == path_adj[4]:
                                if j > i:
                                    list_local_hero.append(path_adj[0])
                                else:
                                    list_local_hero.insert(len(list_local_obj) - 1, path_adj[0])

                    if list_local_obj not in full_list and list_local_obj != []:
                        full_list.append(list_local_obj)
                    if list_local_hero not in full_list and list_local_hero != []:
                        full_list.append(list_local_hero)

                elif path[3] == 'adjobj':
                    temp_word = ['adjobj', path[4]]
                elif path[3] == 'adjhero':
                    temp_word = ['adjhero', path[4]]

        # второй круг, спец для случая если система перепутала признак объекта и субьекта,
        # проходим по базе, в которой уже сняты метки

        # # print(text)
        # # print(list_local_obj, list_local_hero)
        # for i in text_base.columns:
        #     if check_word(text_base[i]):
        #         if text_base[i][3] == 'adjobj' or text_base[i][3] == 'adjhero':
        #             full_list.append([text_base[i][5]])
        #             text_base[i][3] = None

        gigant_list.append(full_list)

    # print(list_local_hero + list_local_obj)

    return text, gigant_list


# строка после чтения сложного списка ержится в обычнгый список
def listmerge_for_strings(lstlst):
    lst = str(lstlst).replace('[', '').replace(']', '').replace(',', '').replace("'", '').split()
    return lst


# текст парсится, бьется на скилы, сверяется со списком скилов, отмечается совпадениями,
# на выходе строка для датафрейма, соответствующая столбцам датафрейма от списка скилов

def match_vacancy_skills_to_skill_list(text, skills_dict, ind,vision=0):
    skill_rate_temp = pd.DataFrame(columns=list(skills_dict.values()))
    # text = data_descriptions.loc[i, 'requirement']
    # text2 = data_descriptions.loc[i, 'descriptions']
    # ind = data_descriptions.loc[i, 'id']
    # # print(ind)
    skill_rate_temp.loc[ind] = 0

    # складываем скилы в базу
    # получаем распарсенное на кусочки описание вакансии
    skills, full_list = reparce_for_skills_listlist_zero(text, vision=vision)

    # здесь плюсуем найденные скилы
    for text_block in full_list:
        if text_block:
            for skills in text_block:
                if skills:
                    for skill in skills:
                        if skill.lower() in skills_dict.values():
                            for j, column in enumerate(skill_rate_temp.columns):
                                if skill == column:
                                    skill_rate_temp[column] += 1

    skill_rate_temp['id'] = ind
    skill_list = list(skill_rate_temp.loc[ind])

    return skill_list


