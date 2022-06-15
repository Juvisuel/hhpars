import requests
import pprint

# 54939886

main_url = 'https://api.hh.ru/'

vacancy = requests.get(main_url+'vacancies/54939886')

pprint.pprint(vacancy.json()['description'])


# неюзанный код от какого-то умного парсинга

# class PythonOrgSearch:
#     """A sample test class to show how page object works"""
#     print(temp_url)
#     def __init__(self):
#         self.main_page = page.MainPage(self.driver)
#
#
#     def setUp(self):
#         self.driver = webdriver.Chrome('F:\learn_neuro\hhpars\driver/chromedriver.exe')
#         self.driver.get(temp_url)
#
#     def test_search_in_python_org(self, main_page):
#         """
#         Tests python.org search feature. Searches for the word "pycon" then verified that some results show up.
#         Note that it does not look for any particular text in search results page. This test verifies that
#         the results were not empty.
#         """
#
#         #Load the main page. In this case the home page of Python.og.
#
#         #Checks if the word "Python" is in title
#
#         assert main_page.is_title_matches(), "python.org title doesn't match."
#         #Sets the text of search textbox to "pycon"
#
#         main_page.search_text_element = "pycon"
#         main_page.click_go_button()
#
#         search_results_page = page.SearchResultsPage(self.driver)
#
#         #Verifies that the results page is not empty
#         assert search_results_page.is_results_found(), "No results found."
#
#     def tearDown(self):
#         self.driver.close()


# search = PythonOrgSearch(temp_url)
# search.main_page.click_go_button()