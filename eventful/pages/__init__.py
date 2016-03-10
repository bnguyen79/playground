import os
import json
import time
import datetime
from datetime import date
import hashlib

from selenium import selenium
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):
    """Eventful BasePage"""

    def __init__(self, driver):
        super(BasePage, self).__init__()
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 20)
        self.timeout = 30

        self.page_elements = []
        self.failed_elements = []

    def __str__(self):
        if self.url:
            print "\nURL: {}\n".format(self.url)

        if self.page_elements:
            print "Page Elements\n"
            for item in self.page_elements:
                print "- {}".format(item)
            print "\n"


    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title

    def navigate_to_join_form(self):
        self.driver.get(self.join_form_url)
        #self.driver.maximize_window()

    def navigate_to_performer_join(self):
        self.driver.get(self.performer_join_url)

    def navigate_to_demand_it_page(self):
        self.driver.get(self.demand_it_url)

    def get_elements(self, locators_dict):
        for name, locator in locators_dict.iteritems():
            try:
                if "text" in name:
                    setattr(self, name, self.driver.find_element(*locator).text)
                elif "list" in name:
                    setattr(self, name, self.driver.find_elements(*locator))
                else:
                    setattr(self, name, self.driver.find_element(*locator))
            except NoSuchElementException:
                self.failed_elements.append(name)
            else:
                self.page_elements.append(name)

    def fill_form_element(self, form_element, value):
        try:
            form_element.clear()
            form_element.send_keys(value)
        except:
            print "Form Element Not Present"

    def set_form_element_text_and_focusout(self, form_element, value, sleep=None):
        form_element.clear()
        form_element.send_keys(value)
        form_element.send_keys(Keys.TAB)

        if sleep:
            time.sleep(sleep)

    def select_from_dropdown(self, dropdown_element, value):
        select = Select(dropdown_element)
        try:
            select.select_by_visible_text(value)
        except NoSuchElementException:
            print "{} is not a valid option. Please try one of the following:\n".format(value)
            for option in select.options:
                print "\t- {}".format(option.text)
            print "\n"
            raise

    def click_and_wait_for_page_load(self, click_element, new_page_element, wait_time=30):
        getattr(self, click_element).click()
        WebDriverWait(self.driver, wait_time).until(lambda driver: driver.find_element(*new_page_element))

    def number_of_windows(self):
        return len(self.driver.window_handles)

    def switch_to_popup_window(self):
        self.wait.until(lambda driver: self.number_of_windows() != 1)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def switch_to_main_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    """
    def underage_month(self):
        today_month = date.today().month
        underage_month = date.today().month-1
        if underage_month <= 0:
            adj_month = 12 + underage_month
            underage_month = adj_month
        underage_dob_month = {
            1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",
            8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        return underage_dob_month[underage_month]
    """

    def underage_month(self):
        underage_month = date.today().month
        underage_dob_month = {
            1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",
            8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        return underage_dob_month[underage_month]

    def underage_day_before(self):
        day_before = date.today().day + 1
        return str(day_before)

    def underage_day_after(self):
        day_after = date.today().day - 1
        return str(day_after)

    def underage_year(self):
        underage_year = date.today().year - 13
        return str(underage_year)

    def all_displayed_page_links(self):
        all_links = self.driver.find_elements_by_tag_name("a")
        all_links_names = []
        for link in all_links:
            if link.is_displayed():
                all_links_names.append(link.text)
        all_links_text_encoded = type(all_links_names)(x.encode('ascii') for x in all_links_names)
        return all_links_text_encoded

    def wait_until_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of(locator))
        except:
            print "Element did not appear - '{}'".format(locator)
            raise TimeoutException

    def wait_until_not_visible(self, locator):
        try:
            self.wait.until_not(EC.visibility_of(locator))
        except TimeoutException:
            print "Element did not go away - '{}'".format(locator)
            raise TimeoutException

    def hover_over(self, element, sleep=None):
        actions = ActionChains(self.driver)
        hover = actions.move_to_element(element)
        hover.perform()
        if sleep:
            time.sleep(sleep)

    def hover_over_then_click(self, element, sleep=None):
        actions = ActionChains(self.driver)
        hover = actions.move_to_element(element)
        if sleep:
            time.sleep(sleep)
        hover.click()
        hover.perform()
