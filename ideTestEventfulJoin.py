# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class IdeTestEventfulJoin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://search.yahoo.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_ide_test_eventful_join(self):
        driver = self.driver
        driver.get(self.base_url + "/yhs/search?p=eventful&ei=UTF-8&hspart=mozilla&hsimp=yhs-002")
        driver.find_element_by_id("yschsp").click()
        driver.find_element_by_id("yui_3_10_0_1_1449092637055_559").click()
        driver.find_element_by_id("yui_3_10_0_1_1449092732910_305").click()
        driver.find_element_by_link_text("Movies").click()
        driver.find_element_by_link_text("Demand it!").click()
        driver.find_element_by_css_selector("#nav-my > a.nav-tab").click()
        driver.find_element_by_css_selector("a > strong").click()
        driver.find_element_by_id("inp-join-email").clear()
        driver.find_element_by_id("inp-join-email").send_keys("qa3eventful@outlook.com")
        driver.find_element_by_id("inp-join-username").clear()
        driver.find_element_by_id("inp-join-username").send_keys("qa3")
        driver.find_element_by_id("inp-password1").click()
        driver.find_element_by_id("inp-password1").clear()
        driver.find_element_by_id("inp-password1").send_keys("qaauto")
        driver.find_element_by_id("inp-join-zipcode").clear()
        driver.find_element_by_id("inp-join-zipcode").send_keys("92020")
        driver.find_element_by_id("btn-mJoin-gender-male").click()
        Select(driver.find_element_by_id("dob_month")).select_by_visible_text("Oct")
        driver.find_element_by_id("dob_day").clear()
        driver.find_element_by_id("dob_day").send_keys("10")
        driver.find_element_by_id("dob_year").clear()
        driver.find_element_by_id("dob_year").send_keys("1979")
        driver.find_element_by_id("inp-mJoin-captcha").clear()
        driver.find_element_by_id("inp-mJoin-captcha").send_keys("HFWXKM")
        driver.find_element_by_id("inp-mJoin-special-offers").click()
        driver.find_element_by_css_selector("label > span").click()
        driver.find_element_by_id("inp-join-submit").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
