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
from selenium.common.exceptions import NoSuchElementException
from nose.tools import *
from nose.plugins.attrib import attr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.join import JoinPage

class TestEventfulFacebookJoinPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        # self.driver = webdriver.Remote(
        #     command_executor='http://prds-selenium02.jfk.ad.radio.com:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME
        # )
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 20)
        cls.join_page = JoinPage(cls.driver)
        cls.join_page.navigate_to_join_form()
        cls.join_page.get_header_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    #TEST FACEBOOOK JOIN PAGE TITLE
    @attr("join","facebook", "title")
    def test_fb_join_page_title(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        time.sleep(0)
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        self.assertEqual(self.driver.title, "Join now - Eventful")

    #TEST FACEBOOK JOIN PAGE URL
    @attr("join","facebook","url")
    def test_fb_join_page_url(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        time.sleep(0)
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/facebook")

    #TEST FACEBOOK JOIN PAGE ELEMENTS
    @attr("join","ui","facebook")
    def test_fb_join_page_elements_displayed(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        jp.get_all_facebook_join_elements()
        #jp.click_fb_okay_btn()     ###this additional screen only appears on 1st use of fb email, even if profile not complete
        self.assertTrue(jp.header_logo.is_displayed())
        self.assertTrue(jp.fb_subheader.is_displayed())
        self.assertTrue(jp.subheader_msg_confirm.is_displayed())
        self.assertTrue(jp.subheader_msg_enter.is_displayed())
        self.assertTrue(jp.subheader_msg_agree.is_displayed())
        self.assertTrue(jp.email_field.is_displayed())
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
        self.assertTrue(jp.opt_in_section.is_displayed())
        self.assertTrue(jp.opt_in_checkbox.is_displayed())
        self.assertTrue(jp.opt_in_pp_link.is_displayed())
        self.assertTrue(jp.opt_in_tou_link.is_displayed())
        self.assertTrue(jp.opt_in_vsp_link.is_displayed())
        self.assertTrue(jp.continue_button.is_displayed())
        self.assertTrue(jp.signin_msg.is_displayed())
        self.assertTrue(jp.signin_link.is_displayed())
        self.assertTrue(jp.performer_signup_msg.is_displayed())
        self.assertTrue(jp.performer_signup_link.is_displayed())
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
        self.assertTrue(jp.city_field.is_displayed())          ###hidden until 'not in us' link clicked
        self.assertTrue(jp.country_dropdown.is_displayed())        ###hidden until 'not in us' link clicked

    #TEST PASSWORD & CAPTCHA FIELDS DO NOT EXIST ON PAGE
    @attr("join","ui","facebook","hidden")
    def test_fb_join_page_elements_hidden(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        #jp.get_all_facebook_join_elements()
        password_field_count = self.driver.find_elements_by_id("inp-password1")
        captcha_field_count = self.driver.find_elements_by_id("inp-mJoin-captcha")
        self.assertEqual(len(password_field_count), 0)
        self.assertEqual(len(captcha_field_count), 0)

    #TEST EMAIL FIELD IS PREFILLED BASED OFF FACEBOOK DATA, ASSERT EMAIL FILED IS NOT EMPTY
    @attr("join","facebook","email")
    def test_facebook_join_email_prefilled(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        jp.get_facebook_join_form()
        self.assertNotEqual(jp.email_field.get_attribute('value'), '')

    #TEST EMAIL FIELD IS PREFILLED WITH CORRECT FACEBOOK EMAIL, ASSERT EMAIL FIELD PREFILL IS SAME AS USED TO LOGIN
    @attr("join","facebook","email")
    def test_facebook_join_email_prefilled_correct_email(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        jp.get_facebook_join_form()
        self.assertEqual(jp.new_facebook_email, jp.email_field.get_attribute('value'))

    #TEST A GENDER IS PRESELECTED BASED OFF FACEBOOK DATA
    @attr("join","facebook","gender")
    def test_facebook_join_gender_preselected(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        jp.get_facebook_join_form()
        gender_buttons = [jp.female_button,jp.male_button]
        gender_buttons_class = []
        for gender in gender_buttons:
            gender_class = gender.get_attribute('class')
            gender_buttons_class.append(gender_class)
        joined_gender_buttons = ''.join(gender_buttons_class)
        print joined_gender_buttons
        self.assertIn("active", joined_gender_buttons)

    #TEST DATE OF BIRTH IS PREFILLED BASED OFF FACEBOOK DATA
    def test_facebook_join_dob_prefilled(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        jp.get_facebook_join_form()
        self.assertNotEqual(jp.dob_month_dropdown.get_attribute('value'), '')
        self.assertNotEqual(jp.dob_day_dropdown.get_attribute('value'), '')
        self.assertNotEqual(jp.dob_year_dropdown.get_attribute('value'), '')

    #TEST USER CAN ENTER DATA AND IS RETAINED
    @attr("join","functional")
    def test_facebook_join_page_fields_test(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        jp.switch_to_popup_window()
        jp.set_facebook_new_email_pass()
        jp.switch_to_main_window()
        time.sleep(2)
        jp.get_facebook_join_form()
        jp.set_email(self.email)
        try:
            if jp.zipcode_field.is_displayed():
                jp.set_zipcode("00022")
                self.assertNotEqual(jp.zipcode_field.get_attribute('value'), '')
            else:
                jp.in_the_us_link.click()
                jp.set_zipcode("00022")
                self.assertNotEqual(jp.zipcode_field.get_attribute('value'), '')
        except:
            pass
        jp.not_in_us_link.click()
        jp.set_city("Vancouver")
        jp.select_country("Canada")
        jp.click_male_button()
        self.assertEqual(jp.male_button.get_attribute('class'), "gender-select left-btn active")
        jp.click_female_button()
        self.assertEqual(jp.female_button.get_attribute('class'), "gender-select right-btn active")
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.click_opt_in_checkbox()
        self.assertEqual(jp.opt_in.get_attribute('class'), "ng-dirty ng-valid ng-valid-required")
        all_fields_list = [jp.email_field,jp.city_field,jp.country_dropdown,jp.dob_month_dropdown,
                           jp.dob_day_dropdown,jp.dob_year_dropdown]
        for field in all_fields_list:
            self.assertNotEqual(field.get_attribute('value'), '')

    """
    #TEST FACEBOOK SIGNUP BUTTON FUNCTION WITH ***unknown user***
    def test_unknown_facebook_signup(self):
        jp = self.join_page
        #fbj = self.facebook_join
        #fbj.navigate_facebook_join()
        #jp._get_joinpage_elements()
        jp.facebook_signup_button.click()
        time.sleep(1)

        #POPUP APPEARS TO ENTER FB CREDENTIALS
        jp.switch_to_popup_window()
        jp.set_facebook_email("binhone_uukjsby_qa@tfbnw.net")
        jp.set_facebook_pass("eventful")
        jp.set_facebook_pass(Keys.TAB)
        jp.set_facebook_pass(Keys.ENTER)

        #CLICK OKAY ON FACEBOOK PERMISSION WINDOW
        #jp.click_fb_okay_btn()     ###SEEMS THIS ONLY APPEARS ON FIRST USE OF A FB EMAIL, WONT APEAR AGAIN EVEN IF USER HASNT COMPLETED PROFILE

        #NEW PAGE FOR USER TO COMPLETE PROFILE
        jp.switch_to_main_window()
        self.complete_profile = self.driver.find_element_by_xpath(".//*[@id='content']//h1[contains(text(), 'Complete your facebook profile')]")
        self.wait.until(EC.visibility_of(self.complete_profile))
        self.assertEqual(self.driver.title, "Join now - Eventful")
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/facebook")
        self.assertTrue(self.complete_profile.is_displayed())
        print 'ok'
        time.sleep(20)

        #jp.switch_to_main_window()
        self.wait.until(lambda driver: jp.build_your_profile)
        #self.wait.until(lambda driver: driver.current_url == "http://eventful/tracker#/")  ###THIS DOESNT WORK, DONT KNOW WHY
        self.assertEqual(self.driver.title, "Eventful Tracker")
        self.assertEqual(self.driver.current_url, "http://eventful.com/tracker#/")
        self.user_panel = self.driver.find_element_by_xpath(".//*[@id='user-panel']")
        self.assertIn("logged-in", self.user_panel.get_attribute('class'))
    """


    #TEST FACEBOOK JOIN PAGE ERROR MSGS