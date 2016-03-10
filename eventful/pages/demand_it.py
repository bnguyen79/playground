import os
import json
import time
import random
from datetime import date
from selenium import selenium
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import BasePage

class DemandIt(BasePage):
    """Eventful Demand page"""

    demand_it_url = "http://eventful.com/demand/hottest"

    def __init__(self, driver):
        super(DemandIt, self).__init__(driver)
        # Page Element Locators
        self.locators = {
            "demand_it_header_elements": {
                "sub_demand_campaigns_link": (By.XPATH, ".//*[@id='sub-demands']//a[text()='Demand it! Campaigns']"),
                "sub_demand_top_local_link": (By.XPATH, ".//*[@id='sub-demands']//a[text()='Top Local Demands']"),
                "sub_demand_top_50_link": (By.XPATH, ".//*[@id='sub-demands']//a[text()='Demand it! Top 50']"),
                "breadcrumbs": (By.XPATH, ".//*[@id='breadcrumb']//span[@class='crumb-path']"),
                "breadcrumbs_home": (By.XPATH, ".//*[@id='breadcrumb']//a[text()='Home']"),
                "breadcrumbs_demand": (By.XPATH, ".//*[@id='breadcrumb']//a[text()='Demand']"),
            },
            "demand_it_chart_elements": {
                "demand_it_chart_header": (By.XPATH, './/*[@id="box-today-hottest-demands"]//h3[text()="Today\'s hottest  demands"]'),
                "demand_it_rankings_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//td[@class='ranking']"),
                "demand_it_no_1": (By.XPATH, ".//*[@id='box-today-hottest-demands']//td[@class='ranking']//span[1]"),
                "demand_it_images_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//img[@class='event-img']"),
                "demand_it_images_links_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//td[@class='photo']/a"),
                "demand_it_title_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//div[@class='left-with-demand-it']/h2/a"),
                "demand_it_description_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//div[@class='left-with-demand-it']/p"),
                "demand_it_demand_it_count_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//a[@class='demand-count']"),
                "demand_it_demand_it_button_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//a[@class='bn demand-lg bn-demand']"),
                "demanded_in_header_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//h3[text()='Demanded in ... ']"),
                "demanded_in_see_all_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//h3/a[text()='See all']"),
                "demanded_in_cities_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//ul[contains(@class, 'top-demands')]/li"),
                "demanded_in_cities_links_list": (By.XPATH, ".//*[@id='box-today-hottest-demands']//ul[contains(@class, 'top-demands')]/li/div/a"),
            },
            "demand_it_right_column_what_is": {
                "what_is_demand_header": (By.ID, "whats-demand"),
                "what_is_demand_1": (By.XPATH, ".//*[@id='demand-process']/dt[1]"),
                "what_is_demand_1_desc": (By.XPATH, ".//*[@id='demand-process']/dd[@class='d1']"),
                "what_is_demand_2": (By.XPATH, ".//*[@id='demand-process']/dt[2]"),
                "what_is_demand_2_desc": (By.XPATH, ".//*[@id='demand-process']/dd[2]"),
                "what_is_demand_3": (By.XPATH, ".//*[@id='demand-process']/dt[3]"),
                "what_is_demand_3_desc": (By.XPATH, ".//*[@id='demand-process']/dd[3]"),
                "demand_your_performer": (By.XPATH, ".//*[@id='demand-picker']//span[text()='Demand your favorite performer']"),
                "demand_your_performer_field": (By.XPATH, ".//input[@id='inp-demand-performer']"),
                "demand_your_performer_demand_button": (By.ID, "demand-picker-demand-it"),
                "demand_your_performer_typeahead": (By.XPATH, ".//*[@id='list-results-demand-performer']"),
                },
            "demand_it_right_column_most_demanding": {
                "most_demanding_header": (By.XPATH, ".//*[@id='box-most-demanding']//h3[text()='Most demanding']"),
                "most_demanding_colleges_header": (By.XPATH, ".//*[@id='box-most-demanding']//h3[text()='Colleges']"),
                "most_demanding_colleges_list": (By.XPATH, ".//*[@id='box-most-demanding']/div[@class='section last']/ul[@class='columnar columns-1 top-demands-college']/li"),
                "most_demanding_colleges_links_list": (By.XPATH, ".//*[@id='box-most-demanding']/div[@class='section last']/ul[@class='columnar columns-1 top-demands-college']//a"),
                "most_demanding_cities_header": (By.XPATH, ".//*[@id='box-most-demanding']//h3[text()='Cities']"),
                "most_demanding_cities_list": (By.XPATH, ".//*[@id='box-most-demanding']//ul[@id='demands-popular-city']/li"),
                "most_demanding_cities_links_list": (By.XPATH, ".//*[@id='box-most-demanding']//ul[@id='demands-popular-city']//a"),
                "not_finding_it": (By.XPATH, ".//*[@id='content']/div[2]//h3[text()='Not finding it?']"),
                "add_a_demand_icon": (By.XPATH, ".//*[@id='content']//div[2]//span[@class='left']"),
                "add_a_demand_link": (By.XPATH, ".//*[@id='content']//div[2]//a[@class='grey']"),
            }
        }

    def get_demand_it_header_elements(self):
        self.get_elements(self.locators["demand_it_header_elements"])

    def get_demand_it_chart_elements(self):
        self.get_elements(self.locators["demand_it_chart_elements"])

    def get_demand_it_right_column_what_is_elements(self):
        self.get_elements(self.locators["demand_it_right_column_what_is"])

    def get_demand_it_right_column_most_demanding_elements(self):
        self.get_elements(self.locators["demand_it_right_column_most_demanding"])

    def get_all_demand_it_page_elements(self):
        self.get_demand_it_header_elements()
        self.get_demand_it_chart_elements()
        self.get_demand_it_right_column_what_is_elements()
        self.get_demand_it_right_column_most_demanding_elements()

    def typeahead_1_character_list(self):
        self.typeahead_1_character_list = ["a", "b", "c", "1", "0", "+", "}", " ",
                                           "-", "@", "?", "*"]
        return self.typeahead_1_character_list

    def typeahead_2_character_list(self):
        self.typeahead_2_character_list = ["be", "me", "xx", "12", "99", "00", "5s",
                                           "0o", "AD", "!@", "<>", "#;"]
        return self.typeahead_2_character_list

    def demand_performers_list(self):
        self.demand_performers_list = ["ace", "the", "nsync", "madonna", "wu", "britt", ""
                                       "cher", "kevin hart", "one", "nicki", "donald", "beyonce", ]
        return self.demand_performers_list

    @property
    def typeahead_popover(self):
        self._typeahead_popover = self.driver.find_element(By.XPATH, "//div[@id='popover-demand-performer']").get_attribute('style')
        return self._typeahead_popover

    @property
    def typeahead_loading_symbol(self):
        self._typeahead_loading_symbol = self.driver.find_element(By.XPATH, "//div[@id='type-ahead-demand-performer']").get_attribute('class')
        return self._typeahead_loading_symbol

    @property
    def demand_your_performer_typeahead_list(self):
        self._demand_your_performer_typeahead_list = self.driver.find_elements_by_xpath(".//*[@id='list-results-demand-performer']/li")
        return self._demand_your_performer_typeahead_list

    @property
    def cant_find_performer_typeahead_result(self):
        self._cant_find_performer_typeahead_result = self.driver.find_element_by_xpath(".//*[@id='list-results-demand-performer']//li[contains(text(), 'Add them!')]")
        return self._cant_find_performer_typeahead_result

    @property
    def bold_characters_in_typeahead(self):
        self._bold_characters_in_typeahead =  self.driver.find_elements_by_xpath(".//*[@id='list-results-demand-performer']/li/b")
        return self._bold_characters_in_typeahead

    def click_demand_your_perfomer_field(self):
        self.demand_your_performer_field.click()

    def click_demand_your_performer_demand_button(self):
        self.demand_your_performer_demand_button.click()

    def set_demand_your_performer(self, value):
        self.fill_form_element(self.demand_your_performer_field, value)

    def get_random_performer_typeahead(self):
        performers_len = len(self.demand_your_performer_typeahead_list)
        index = random.choice(range(0,performers_len-1))
        random_performer = self.demand_your_performer_typeahead_list[index]
        return random_performer

    def click_random_performer_typeahead(self):
        performers_len = len(self.demand_your_performer_typeahead_list)
        index = random.choice(range(0,performers_len-1))
        self.demand_your_performer_typeahead_list[index].click()

    def name_of_random_performer(self):
        performers_len = len(self.demand_your_performer_typeahead_list)
        index = random.choice(range(0,performers_len-1))
        parent = self.demand_your_performer_typeahead_list[index]
        child = parent.find_element_by_class_name('diminished')
        return parent.text.replace(child.text, '')



