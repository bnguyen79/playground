import os
import json
import time
from datetime import date
from selenium import selenium
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from pages import BasePage

class EventfulSite(BasePage):
    """Eventful Site"""

    eventful_url = "http:www.eventful.com"

    def __init__(self, driver):
        super(EventfulSite, self).__init__(driver)
        # Page Element Locators
        self.locators = {
            "header": {
                "eventful_logo": (),
                "location_field": (),
                "find_field": (),
                "search_icon": (),
                "sign_up_link": (),
                "sign_in_link": ()
            },
            "category_tabs": {
                "events_tab": (),
                "movies_tab": (),
                "demand_it_tab": (),
                "my_eventful_tab": (),
            },
            "footer": {

            }

        }
