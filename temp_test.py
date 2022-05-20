import requests
import pprint

# 54939886

main_url = 'https://api.hh.ru/'

vacancy = requests.get(main_url+'vacancies/54939886')

pprint.pprint(vacancy.json()['description'])