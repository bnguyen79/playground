import unittest
import os, sys
import random
import string
import json

from selenium import webdriver
from selenium.webdriver.support import ui

from test_data import TEST_ENV, BROWSER, get_url



class CBSUnitTest(unittest.TestCase):

    def setUp_utils(self, file_name):

        if 'win' in sys.platform:
            driver_path = os.path.join(os.path.dirname(__file__), os.pardir, "drivers", "chromedriver.exe")
        if 'darwin' in sys.platform:
            driver_path = os.path.join(os.path.dirname(__file__), os.pardir, "drivers", "chromedriver 7")

        self.driver = webdriver.Chrome(driver_path)

        url_data = self.get_test_data(file_name, "urls")
        baseurl = get_url(url_data)

        print "\nBase URL: {}\n".format(baseurl)

        self.driver.get(baseurl)
        wait_time = self.get_test_data(file_name, "wait_time")[TEST_ENV]
        print "Wait Time: ", wait_time, " seconds\n\n"
        wait = ui.WebDriverWait(self.driver, wait_time)
        if TEST_ENV != "dev":
            wait.until(lambda driver: self.driver.find_element_by_css_selector("#sso-iframe-wrapper > iframe"))
            self.driver.switch_to_frame(self.driver.find_element_by_css_selector("#sso-iframe-wrapper > iframe"))

    def get_test_data(self,file_name, json_key):
        with open(file_name) as f:
            json_as_string = f.read()
        body = json.loads(json_as_string)
        itemlist = body[json_key]
        return itemlist

    def get_random_string(self,length):
        return ''.join(random.choice(string.ascii_letters) for x in range(length))

    def get_random_email_address(self):
        return "qatest_" + self.get_random_string(20) +"@qa.com"

    def get_random_first_name(self):
        return "first" + self.get_random_string(15)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()