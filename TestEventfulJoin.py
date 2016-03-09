# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class IdeTestEventfulJoin(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome('/Users/bnguyen/Documents/tools/chromedriver.exe')
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.eventful.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_ide_test_eventful_join(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.maximize_window()
        #driver.find_element_by_link_text("Movies").click()
        #driver.find_element_by_link_text("Demand it!").click()
        driver.find_element_by_css_selector("#nav-my > a.nav-tab").click()
        driver.find_element_by_css_selector("a > strong").click()


        ###     EMAIL ADDRESS
        driver.find_element_by_id("inp-join-email").clear()
        existing_email = ["qa3eventful@outlook.com", "ladyhoopz31@yahoo.com", "daisies4drew@yahoo.com"]
        new_email = ["qa4eventful@outlook.com", "qa55eventful@outlook.com", "qa66eventful@outlook.com"]
        invalid_email = ["p", "event.com", "!!@", "hot@here", "1@1.1", " space @here.com", " space@here.com"]

        driver.find_element_by_id("inp-join-email").send_keys(invalid_email[4])
        driver.find_element_by_id("inp-join-email").send_keys(Keys.TAB)
        entered_email = driver.find_element_by_id("inp-join-email").get_attribute('value')
        existing_email_error_msg = driver.find_element_by_xpath(".//*[@id='content']/div/div/div/div/form/div[2]")
        invalid_email_error_msg = driver.find_element_by_xpath(".//*[@id='content']/div/div/div/div/form/div[1]")
        if existing_email_error_msg.is_displayed():
            print "'Known Email Address.' message is displayed" + " - (" + entered_email + ")"
        elif invalid_email_error_msg.is_displayed():
            print "'Sorry, this doesn't look like a valid email address.' is displayed"  + " - (" + entered_email + ")"
        else:
            #print "Missing 'Known Email Address.' message" + " - (" + entered_email + ")"
            print "No email error message" + " - (" + entered_email + ")"


        ###     USERNAME
        existing_username = ["qa3", "qa2", "www"]       #existing username in DB
        new_username = ["qa4", "qa41", "qa412", "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqweq"]         #username not in DB
        invalid_username = ["a", "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqweqw", "333", "!@#", "   "]

        driver.find_element_by_id("inp-join-username").clear()
        driver.find_element_by_id("inp-join-username").send_keys(invalid_username[4])
        driver.find_element_by_id("inp-password1").click()
        driver.find_element_by_id("inp-password1").clear()

        entered_username = driver.find_element_by_id("inp-join-username").get_attribute('value')
        #existing_username = driver.find_element_by_xpath(".//*[@id='content']/div/div/div/div/form/div[4]")
        #too_short_username = driver.find_element_by_xpath(".//*[@id='content']/div/div/div/div/form/div[4]")
        username_error_msg = driver.find_element_by_xpath(".//*[@id='content']/div/div/div/div/form/div[4]").text
        username_error_msg1 = driver.find_element_by_xpath(".//*[@id='content']/div/div/div/div/form/div[3]").text
        if username_error_msg == "Username is already taken":
            print "'Username is already taken' message is displayed" + " - (" + entered_username + ")"
        elif username_error_msg == "Your username is too short (Min length:3)":
            print "'Your username is too short (Min length:3)' message is displayed" + " - (" + entered_username + ")"
        elif username_error_msg == "Your username is too long (Max length:64)":
            print "'Your username is too long (Max length:64)' message is displayed" + " - (" + entered_username + ")"
        elif username_error_msg == "Your username can not contain only numbers":
            print "'Your username can not contain only numbers' message is displayed" + " - (" + entered_username + ")"
        elif username_error_msg == "Your username is invalid, please try again.":
            print "'Your username is invalid, please try again.' message is displayed" + " - (" + entered_username + ")"
        elif username_error_msg1 == "Sorry, a username must be between 2 and 10 characters.":
            print "'Sorry, a username must be between 2 and 10 characters.' message is displayed" + " - (" + entered_username + ")"
        else:
            print "No Username error message" + " - (" + entered_username + ")"



        ###     PASSWORD
        invalid_password = ["1", "22", "33"]
        valid_password = ["123", "qqq", "!@#$$%%^^&"]

        driver.find_element_by_id("inp-password1").send_keys(invalid_password[2])
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
