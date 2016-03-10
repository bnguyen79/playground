# -*- coding: utf-8 -*-
import json
import time
import datetime
from datetime import date
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from nose.tools import *
from nose.plugins.attrib import attr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.join import JoinPage

class TestEventfulPerformerJoinPage(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Firefox()
        # self.driver = webdriver.Remote(
        #     command_executor='http://prds-selenium02.jfk.ad.radio.com:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME
        # )
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 20)
        cls.join_page = JoinPage(cls.driver)
        cls.join_page.navigate_to_performer_join()
        cls.join_page.get_performer_sign_up_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()

    #TEST PERFORMER JOIN PAGE TITLE
    @attr("join","performer", "title")
    def test_performer_join_page_title(self):
        self.assertEqual(self.driver.title, "Join now - Eventful")

    #TEST PERFORMER JOIN PAGE URL
    @attr("join","performer", "url")
    def test_performer_join_page_url(self):
        self.assertEqual(self.join_page.current_url, "http://eventful.com/join?as=performer#/")

    #TEST PERFORMER JOIN PAGE ELEMENTS ARE DISPLAYED
    @attr("join","performer", "ui")
    def test_performer_join_page_elements_displayed(self):
        jp = self.join_page
        self.assertTrue(jp.header_logo.is_displayed())
        self.assertTrue(jp.performer_signup_subheader.is_displayed())
        self.assertTrue(jp.facebook_signup_button.is_displayed())
        self.assertTrue(jp.or_msg.is_displayed())
        self.assertTrue(jp.signup_subheader.is_displayed())
        self.assertTrue(jp.email_field.is_displayed())
        self.assertTrue(jp.password_field.is_displayed())
        self.assertTrue(jp.zipcode_field.is_displayed())
        self.assertEqual(jp.city_field.get_attribute('class'), "input international ng-pristine ng-valid ng-hide")      #assert hidden
        self.assertEqual(jp.country_dropdown.get_attribute('class'), "input international empty ng-pristine ng-valid ng-hide")  #assert hidden
        self.assertTrue(jp.not_in_us_link.is_displayed())
        self.assertEqual(jp.not_in_us_link.text, "Not in the US?")
        self.assertTrue(jp.male_button.is_displayed())
        self.assertTrue(jp.female_button.is_displayed())
        self.assertTrue(jp.date_of_birth_msg.is_displayed())
        self.assertTrue(jp.dob_month_dropdown.is_displayed())
        self.assertTrue(jp.dob_day_dropdown.is_displayed())
        self.assertTrue(jp.dob_year_dropdown.is_displayed())
        self.assertTrue(jp.captcha_field.is_displayed())
        self.assertTrue(jp.opt_in_checkbox.is_displayed())
        self.assertTrue(jp.opt_in_section.is_displayed())
        self.assertTrue(jp.opt_in_pp_link.is_displayed())
        self.assertTrue(jp.opt_in_tou_link.is_displayed())
        self.assertTrue(jp.opt_in_vsp_link.is_displayed())
        self.assertTrue(jp.continue_button.is_displayed())
        self.assertTrue(jp.signin_msg.is_displayed())
        self.assertTrue(jp.signin_link.is_displayed())
        self.assertTrue(jp.footer_links_section.is_displayed())
        self.assertTrue(jp.video_services_policy.is_displayed())
        self.assertTrue(jp.video_services_policy_link.is_displayed())
        self.assertTrue(jp.cbs_local_logo.is_displayed())
        self.assertTrue(jp.radiocom_logo.is_displayed())
        self.assertTrue(jp.copyright.is_displayed())
        jp.not_in_us_link.click()
        self.assertTrue(jp.in_the_us_link.is_displayed())
        self.assertEqual(jp.in_the_us_link.text, "In the US?")
        self.assertEqual(jp.zipcode_field.get_attribute('class'), "ng-pristine ng-valid-minlength ng-valid ng-valid-required")  #assert hidden
        self.assertTrue(jp.city_field.is_displayed())          ###this field hidden until 'not in us link' clicked
        self.assertTrue(jp.country_dropdown.is_displayed())        ###this field hidden until 'not in us link' clicked

    #TEST PERFORMER SIGN UP MSG & LINK DO NOT EXIST ON PAGE
    @attr("join","performer", "ui", "hidden")
    def test_performer_join_page_elements_hidden(self):
        performer_signup_msg_count = self.driver.find_elements_by_xpath("//p[@class='signin-link' and contains(text(),'Are you a performer?')]")
        performer_signup_link = self.driver.find_elements_by_id("#performer-join")
        self.assertEqual(len(performer_signup_msg_count), 0)
        self.assertEqual(len(performer_signup_link), 0)