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

class TestEventfulJoinPage(unittest.TestCase):

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
        cls.join_page.get_all_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


    #TEST JOIN PAGE HAS CORRECT TITLE
    @attr("join", "title")
    def test_01_join_page_title(self):
        self.assertEqual(self.join_page.title, "Join now - Eventful")

    #TEST JOIN PAGE HAS CORRECT URL
    @attr("join", "url")
    def test_02_Join_page_url(self):
        self.assertEqual(self.join_page.current_url, "http://eventful.com/join#/")

    #TEST ALL PAGE ELEMENTS ARE DISPLAYED
    @attr("join", "ui", "this")
    def test_03_join_page_ui_elements_present(self):
        jp = self.join_page
        # ---- Header Section ----
        self.assertTrue(jp.header_logo.is_displayed())
        self.assertTrue(jp.subheader.is_displayed())
        # ---- Join Form Section ----
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
        self.assertTrue(jp.performer_signup_msg.is_displayed())
        self.assertTrue(jp.performer_signup_link.is_displayed())
        # ---- Footer Section ----
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

    #TEST USER CAN ENTER DATA AND IS RETAINED
    @attr("join", "functional", "this")
    def test_04_join_page_fields_test(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
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
        jp.set_captcha("EHXSQG")
        jp.click_opt_in_checkbox()
        self.assertEqual(jp.opt_in.get_attribute('class'), "ng-dirty ng-valid ng-valid-required")
        all_fields_list = [jp.email_field,jp.password_field,jp.city_field,jp.country_dropdown,jp.dob_month_dropdown,
                           jp.dob_day_dropdown,jp.dob_year_dropdown,jp.captcha_field]
        for field in all_fields_list:
            self.assertNotEqual(field.get_attribute('value'), '')

class TestEventfulJoinPageFunctional(unittest.TestCase):

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
        cls.join_page.navigate_to_join_form()
        cls.join_page.get_all_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()

    #TEST USER CAN REGISTER SUCCESSFULLY & SHOWN JOIN SUCCESS PAGE
    @attr("join","funtional","success")
    def test_05_join_page_signup_success_page_shown(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_decoded_captcha()
        jp.click_opt_in_checkbox()
        jp.click_continue_button()
        self.wait.until(EC.title_is("Join Success"))
        self.assertEqual(self.driver.title, "Join Success")
        self.assertEqual(self.driver.current_url, "http://eventful.com/join/join-success")

    #TEST JOIN SUCCESS PAGE DISPLAYS ALL ELEMENTS
    @attr("join","funtional","success")
    def test_06_join_page_signup_success_page_all_elements(self):
        jp = self.join_page
        self.driver.get("http://eventful.com/join/join-success")
        self.wait.until(EC.title_is("Join Success"))
        jp.get_join_success_elements()
        self.assertTrue(jp.eventful_logo.is_displayed())
        self.assertTrue(jp.throbber.is_displayed())
        self.assertTrue(jp.thanks_for_joining.is_displayed())
        self.assertTrue(jp.joined_successfully.is_displayed())
        self.assertTrue(jp.change_username_msg.is_displayed())
        self.assertTrue(jp.click_to_continue_msg.is_displayed())
        self.assertEqual(jp.click_to_continue_msg.text, "Click Continue or wait a few seconds to be automatically redirected")
        self.assertTrue(jp.click_to_continue_link.is_displayed())

    #TEST USER CAN REGISTER SUCCESSFULLY & LANDS ON BULD YOUR PROFILE PAGE
    @attr("join","funtional","success")
    def test_07_join_page_signup_success(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_decoded_captcha()
        jp.click_opt_in_checkbox()
        jp.click_continue_button()
        self.wait.until(lambda driver: jp.build_your_profile)
        self.assertEqual(self.driver.current_url, "http://eventful.com/tracker")

    #TEST UNDERAGE CUTOFF LOGIC 1 DAY BEFORE USER TURNS 13 AND IS BLOCKED
    @attr("join","functional","dob","underage")
    def test_08_join_page_underage_1_day_before_dob(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month(jp.underage_month())
        jp.select_day(jp.underage_day_before())
        jp.select_year(jp.underage_year())
        jp.set_decoded_captcha()
        jp.click_opt_in_checkbox()
        jp.click_continue_button()
        self.wait.until(lambda driver: jp.underage_error.is_displayed())
        self.assertEqual(self.driver.current_url, "http://eventful.com/agerestriction#/")
        self.assertEqual(self.driver.title, "Sign up error")

    #TEST UNDERAGE CUTOFF LOGIC ON EXACT DAY USER TURNS 13
    @attr("join","functional","dob","underage","success")
    def test_09_join_page_underage_on_dob(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month(jp.underage_month())
        jp.select_day(str(date.today().day))
        jp.select_year(jp.underage_year())
        jp.set_decoded_captcha()
        jp.click_opt_in_checkbox()
        jp.click_continue_button()
        self.wait.until(lambda driver: jp.build_your_profile)
        self.assertEqual(self.driver.title, "Eventful Tracker")
        self.assertEqual(self.driver.current_url, "http://eventful.com/tracker")

    #TEST UNDERAGE CUTOFF LOGIC 1 DAY AFTER USER TURNS 13
    @attr("join","functional","dob","underage", "success")
    def test_10_join_page_underage_1_day_after_dob(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month(jp.underage_month())
        jp.select_day(jp.underage_day_after())
        jp.select_year(jp.underage_year())
        jp.set_decoded_captcha()
        jp.click_opt_in_checkbox()
        jp.click_continue_button()
        self.wait.until(lambda driver: jp.build_your_profile)
        self.assertEqual(self.driver.title, "Eventful Tracker")
        self.assertEqual(self.driver.current_url, "http://eventful.com/tracker")

    #TEST UNDERAGE COOKIE IS SET WHEN UNDERAGE USER ATTEMPTS TO JOIN
    @attr("join","functional","dob","underage","cookie")
    def test_11_join_page_underage_set_cookie(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month(jp.underage_month())
        jp.select_day(jp.underage_day_before())
        jp.select_year(jp.underage_year())
        jp.set_decoded_captcha()
        jp.click_opt_in_checkbox()
        jp.click_continue_button()
        self.wait.until(lambda driver: jp.underage_error.is_displayed())
        jp.underage_error.send_keys(Keys.CONTROL + 't')
        self.driver.get("http://eventful.com/qatools/cookies")
        time.sleep(0)
        self.assertTrue(jp.underage_cookie.is_displayed())

    #TEST EMAIL FIELD USING VALID FULL TOP LEVEL DOMAINS, ASSERT NO ERROR IS DISPLAYED
    @attr("join","functional","email")
    def test_12_join_page_email_field_valid_tld(self):
        jp = self.join_page
        for tld in jp.valid_email_tld_list():
            valid_tld_email = "qa3eventful+{}@outlook.{}".format(self.now,tld)
            jp.set_email_and_focusout(valid_tld_email)
            print "TESTING - {}".format(valid_tld_email)
            self.assertNotIn("input-error", jp.email_field.get_attribute('class'))

    #TEST EMAIL FIELD USING ANY 2 LETTER TOP LEVEL DOMAINS ARE VALID, ASSERT NO ERROR IS DISPLAYED
    @attr("join","functional","email")
    def test_13_join_page_email_field_valid_2_letter_tld(self):
        jp = self.join_page
        for tld in jp.valid_email_2_character_tld_list():
            valid_tld_email = "qa3eventful+{}@outlook.{}".format(self.now,tld)
            jp.set_email_and_focusout(valid_tld_email)
            print "TESTING - {}".format(valid_tld_email)
            self.assertNotIn("input-error", jp.email_field.get_attribute('class'))

    #TEST EMAIL FIELD USING INVALID TOP LEVEL DOMAINS, ASSERT ERROR IS DISPLAYED
    @attr("join","functional","email")
    def test_14_join_page_email_field_invalid_tld(self):
        jp = self.join_page
        for tld in jp.invalid_email_tld():
            invalid_tld_email = "qa3eventful+{}@outlook.{}".format(self.now,tld)
            jp.set_email_and_focusout(invalid_tld_email)
            print "TESTING - {}".format(invalid_tld_email)
            self.assertIn("input-error", jp.email_field.get_attribute('class'))

    #TEST EMAIL FIELD USING VALID LOCAL PART OF EMAIL, ASSERT NO ERROR IS DISPLAYED
    @attr("join","functional","email")
    def test_15_join_page_email_field_valid_local(self):
        jp = self.join_page
        for email in jp.valid_email_local_list():
            jp.set_email_and_focusout(email)
            print "TESTING - {}".format(email)
            self.assertNotIn("input-error", jp.email_field.get_attribute('class'))

    #TEST EMAIL FIELD USING INVALID EMAIL, ASSERT ERROR IS DISPLAYED
    @attr("join","functional","email")
    def test_16_join_page_email_invalid(self):
        jp = self.join_page
        for email in jp.invalid_email_list():
            jp.set_email_and_focusout(email)
            print "TESTING - {}".format(email)
            self.assertIn("input-error", jp.email_field.get_attribute('class'))

    #TEST PASSWORD FIELD USING VALID PASSWORDS, ASSERT NO ERROR IS DISPLAYED
    @attr("join","functional","password")
    def test_17_join_page_password_field_valid(self):
        jp = self.join_page
        for password in jp.valid_password_list():
            jp.set_email(self.email)
            jp.set_password_and_focusout(password)
            print "TESTING - {}".format(password)
            self.assertNotIn("input-error", jp.password_field.get_attribute('class'))

class TestEventfulJoinPageErrors(unittest.TestCase):

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
        cls.join_page.navigate_to_join_form()
        cls.join_page.get_form_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDown(cls):
        cls.now = None
        cls.email = None
        cls.username = None
        cls.driver.quit()

    #TEST ERROR MESSAGE WHEN EMAIL FIELD IS LEFT BLANK
    @attr("join", "empty", "errors")
    def test_email_empty(self):
        jp = self.join_page
        jp.set_email_and_focusout(Keys.SPACE)
        self.wait.until(lambda driver: jp.email_error_msg.is_displayed())
        self.assertIn("input-error", jp.email_field.get_attribute('class'))
        self.assertTrue(self.join_page.email_error_msg.is_displayed())
        self.assertEqual(self.join_page.email_error_msg.text, "Sorry, this doesn't look like a valid email address.")

    #TEST EMAIL ERROR MESSAGE WHEN EMAIL DOESNT MEET REQUIREMENTS
    @attr("join", "email", "errors")
    def test_email_invalid(self):
        jp = self.join_page
        for invalid_email in jp.invalid_email_list():
            jp.set_email_and_focusout(invalid_email)
            self.wait.until(lambda driver: jp.email_error_msg.is_displayed)
            self.assertIn("input-error", jp.email_field.get_attribute('class'))
            self.assertTrue(jp.email_error_msg.is_displayed())
            self.assertEqual(jp.email_error_msg.text, "Sorry, this doesn't look like a valid email address.")

    #TEST EMAIL ERROR MESSAGE WHEN USER ENTERS A KNOWN EMAIL
    @attr("join", "email", "errors")
    def test_email_known(self):
        jp = self.join_page
        for known_email in jp.known_email_list():
            jp.set_email_and_focusout(known_email)
            self.wait.until(lambda driver: jp.email_error_msg.is_displayed)
            self.assertIn("input-error", jp.email_field.get_attribute('class'))
            self.assertTrue(jp.email_error_msg.is_displayed())
            self.assertEqual(jp.email_error_msg.text, "Known Email Address.")

    #TEST PASSWORD ERROR MESSAGE WHEN PASSWORD ENTERED DOESNT MEET REQUIREMENTS
    @attr("join", "password", "errors")
    def test_password_invalid(self):
        jp = self.join_page
        for invalid_password in jp.invalid_password_list():
            jp.set_password_and_focusout(invalid_password)
            print "TESTING - {}".format(invalid_password)
            self.wait.until(lambda driver: jp.password_error_msg.is_displayed)
            self.assertIn("input-error", jp.password_field.get_attribute('class'))
            self.assertTrue(jp.password_error_msg.is_displayed())
            self.assertEqual(jp.password_error_msg.text, "Please enter at least a 6 character password.")

    #TEST ZIPCODE ERROR MSG WHEN FIELD IS LEFT BLANK
    def test_zipcode_empty(self):
        jp = self.join_page
        jp.set_zipcode_and_focusout(Keys.SPACE)
        self.assertIn("input-error", jp.zipcode_field.get_attribute('class'))
        self.assertTrue(jp.zipcode_error_msg.is_displayed())
        self.assertEqual(jp.zipcode_error_msg.text, "Sorry, this doesn't look like a valid zipcode.")

    #TEST ZIPCODE ERROR MESSAGE WHEN ZIPCODE ENTERED DOESNT MEET REQUIREMENTS
    @attr("join", "zipcode", "errors")
    def test_zipcode_invalid(self):
        jp = self.join_page
        for invalid_zip in jp.invalid_zip_list():
            jp.set_zipcode_and_focusout(invalid_zip)
            self.wait.until(lambda driver: jp.zipcode_error_msg.is_displayed)
            self.assertIn("input-error", jp.zipcode_field.get_attribute('class'))
            self.assertTrue(jp.zipcode_error_msg.is_displayed())
            self.assertEqual(jp.zipcode_error_msg.text, "Sorry, this doesn't look like a valid zipcode.")

    #TEST ZIPCODE ERROR MESSAGE WHEN ZIPCODE ENTERED CONTAINS LETTERS
    @attr("join", "zipcode", "errors")
    def test_zipcode_invalid_alpha(self):
        jp = self.join_page
        for alpha_zip in jp.invalid_alpha_zipcode_list():
            jp.set_zipcode_and_focusout(alpha_zip)
            self.wait.until(lambda driver: jp.zipcode_error_msg.is_displayed)
            self.assertIn("input-error", jp.zipcode_field.get_attribute('class'))
            self.assertTrue(self.join_page.zipcode_error_msg.is_displayed())
            self.assertEqual(self.join_page.zipcode_error_msg.text, "Sorry, this doesn't look like a valid zipcode.")

    #TEST ZIPCODE ERROR MESSAGE WHEN ZIPCODE ENTERED IS NOT RECOGNIZED
    @attr("join", "zipcode", "errors")
    def test_zipcode_unknown(self):
        jp = self.join_page
        for unknown_zip in jp.unknown_zipcode_list():
            jp.set_zipcode_and_focusout(unknown_zip)
            self.wait.until(lambda driver: jp.zipcode_error_msg.is_displayed)
            self.assertIn("input-error", jp.zipcode_field.get_attribute('class'))
            self.assertTrue(jp.zipcode_error_msg.is_displayed())
            self.assertEqual(jp.zipcode_error_msg.text, "unknown location")

    #TEST FOR CAPTCHA ERROR MSG WHEN ENTERED INCORRECTLY
    def test_captcha_incorrect(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("00022")
        jp.not_in_us_link.click()
        jp.set_city("Saskatchewan")
        jp.select_country("Canada")
        jp.click_male_button()
        jp.click_female_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        jp.click_continue_button()
        self.wait.until(lambda driver: jp.captcha_error_msg.is_displayed)
        self.assertIn("input-error", jp.captcha_field.get_attribute('class'))
        self.assertTrue(jp.captcha_error_msg.is_displayed)
        self.assertIn("Captcha incorrect", jp.captcha_error_msg.text)

    #TEST TO MAKE SURE CAPTCHA WILL TIME OUT AFTER 3 MINUTES & DISPLAYS CORRECT MSG
    def test_capthca_after_timeout(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("00022")
        jp.not_in_us_link.click()
        jp.set_city("Saskatchewan")
        jp.select_country("Canada")
        jp.click_male_button()
        jp.click_female_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(181)
        jp.click_continue_button()
        self.wait.until(lambda driver: jp.captcha_error_msg.is_displayed)
        self.assertIn("input-error", jp.captcha_field.get_attribute('class'))
        self.assertTrue(jp.captcha_error_msg.is_displayed)
        self.assertIn("Captcha timeout", jp.captcha_error_msg.text)

    #TEST TO MAKE SURE CAPTCHA WILL NOT TIMEOUT BEFORE 3 MINUTES & SHOWS INCORRECT CAPTCHA MSG
    def test_capthca_before_timeout(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("00022")
        jp.not_in_us_link.click()
        jp.set_city("Saskatchewan")
        jp.select_country("Canada")
        jp.click_male_button()
        jp.click_female_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(179)
        jp.click_continue_button()
        self.wait.until(lambda driver: jp.captcha_error_msg.is_displayed)
        self.assertIn("input-error", jp.captcha_field.get_attribute('class'))
        self.assertTrue("Captcha incorrect", jp.captcha_error_msg.text)

class TestEventfulJoinContinueButton(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Firefox()
        # self.driver = webdriver.Remote(
        #     command_executor='http://prds-selenium02.jfk.ad.radio.com:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME
        # )
        cls.driver.implicitly_wait(10)
        cls.join_page = JoinPage(cls.driver)
        cls.join_page.navigate_to_join_form()
        cls.join_page.get_form_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDown(cls):
        cls.now = None
        cls.email = None
        cls.username = None
        cls.driver.quit()

    #TEST CONTINUE BUTTON IS DISABLED AND INACTIVE WHEN JOIN PAGE FIRST OPENS
    @attr("join", "functional", "continue_btn")
    def test_continue_btn_inactive_to_start(self):
        jp = self.join_page
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")

    #TEST CONTINUE BUTTON DOESNT ACTIVATE UNTIL ALL FIELDS COMPLETE
    @attr("join", "functional", "continue_btn")
    def test_continue_btn_inactive_with_empty_fields(self):
        jp = self.join_page
        jp.set_email(self.email)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.set_password("qaauto")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.set_zipcode("00022")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_male_button()
        self.assertFalse(jp.continue_button.is_enabled())
        jp.select_month("Feb")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.select_day("1")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.select_year("1980")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.set_captcha("LESIGH")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON DOESNT ACTIVATE UNTIL ALL FIELDS COMPLETE WITH CITY/COUNTRY FIELDS DISPLAYED
    #existing bug (test will FAIL) - city/country fields not selected
    @attr("join", "functional", "continue_btn")
    def test_continue_btn_inactive_with_empty_fields_city_country(self):
        jp = self.join_page
        jp.set_email(self.email)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.set_password("qaauto")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.not_in_us_link.click()                           #reveals city/country fields
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_male_button()
        self.assertFalse(jp.continue_button.is_enabled())
        jp.select_month("Feb")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.select_day("1")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.select_year("1980")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.set_captcha("LESIGH")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_opt_in_checkbox()
        self.assertFalse(jp.continue_button.is_enabled())   #city/country fields are still blank and continue button should be disabled

    #TEST CONTINUE BUTTON DOESNT ACTIVATE UNTIL ALL FIELDS COMPLETE
    @attr("join", "functional", "continue_btn")
    def test_continue_btn_activates_when_form_complete(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("00022")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE WILL NOT ACTIVATE WITHOUT EMAIL ADDRESS
    @attr("join", "functional", "continue_btn", "email")
    def test_continue_btn_inactive_email_none(self):
        jp = self.join_page
        jp.set_password("qaauto")
        jp.set_zipcode("00022")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_email_and_focusout(Keys.SPACE)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_email(self.email)
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE WILL NOT ACTIVATE WITH INVALID EMAIL
    @attr("join", "functional", "continue_btn", "email")
    def test_continue_btn_inactive_email_invalid(self):
        jp = self.join_page
        jp.set_password("qaauto")
        jp.set_zipcode("00022")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        jp.set_email("hello")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_email("hello@there")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_email("hello@there.c")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_email("hello@there.comm")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_email(self.email)
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())


    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT PASSWORD
    @attr("join", "functional", "continue_btn", "password")
    def test_continue_btn_inactive_password_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_zipcode("00022")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_password("qaauto")
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITH INVALID PASSWORD
    @attr("join", "functional", "continue_btn", "password")
    def test_continue_btn_inactive_password_invalid(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_zipcode("00022")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        jp.set_password("qaaut")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_password_and_focusout("qaaut")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_password("qaauto")
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT VALID ZIPCODE
    @attr("join", "functional", "continue_btn", "zipcode")
    def test_continue_btn_inactive_zip_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_zipcode_and_focusout(Keys.SPACE)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_zipcode("92131")
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITH SHORT ZIPCODE
    @attr("join", "functional", "continue_btn", "zipcode")
    def test_continue_btn_inactive_zip_short(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        jp.set_zipcode("9213")
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_zipcode("92131")
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITH SPACES IN ZIPCODE  (contains space, no error msg, continue btn active)
    #existing bug (test will FAIL)- field will accept spaces as long as its at least 5 charcters and include 1 number or letter
    @attr("join", "functional", "continue_btn", "zipcode")
    def test_continue_btn_inactive_zip_spaces(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        jp.set_zipcode("z z 9")
        self.assertFalse(jp.continue_button.is_enabled())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITH LETTERS IN ZIPCODE  (at least 5 characters, has error msg, continue btn active)
    #existing bug (test will FAIL)- field will accept more than 5 numbers or letters
    @attr("join", "functional", "continue_btn", "zipcode")
    def test_continue_btn_inactive_zip_long(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        jp.set_zipcode("123abc")
        self.assertFalse(jp.continue_button.is_enabled())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITH SYMBOLS IN ZIPCODE  (at least 5 characters, has error msg, continue btn active)
    #existing bug (test will FAIL)- field will accept symbols as long as at least 1 number or letter
    @attr("join", "functional", "continue_btn", "zipcode")
    def test_continue_btn_inactive_zip_symbols(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        jp.set_zipcode("a!@#$")
        self.assertFalse(jp.continue_button.is_enabled())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT VALID CITY (blank field, no error msg, continue btn active)
    #existing bug (test will FAIL) - field will accept blank
    @attr("join", "functional", "continue_btn", "city")
    def test_continue_btn_inactive_city_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.not_in_us_link.click()
        jp.select_country("Armenia")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT COUNTRY SELECTED (no country selected, no error msg, continue btn active)
    #existing bug (test will FAIL) - country selection not made
    @attr("join", "functional", "continue_btn", "country")
    def test_continue_btn_inactive_country_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.not_in_us_link.click()
        jp.set_city("Amsterdam")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT A GENDER SELECTED
    @attr("join", "functional", "continue_btn", "gender")
    def test_continue_btn_inactive_gender_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.click_male_button()
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT A MONTH OF BIRTH SELECTED
    @attr("join", "functional", "continue_btn", "dob")
    def test_continue_btn_inactive_dob_month_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.select_month("Feb")
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT A DAY OF BIRTH SELECTED
    @attr("join", "functional", "continue_btn", "dob")
    def test_continue_btn_inactive_dob_day_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.select_day("1")
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT A YEAR OF BIRTH SELECTED
    @attr("join", "functional", "continue_btn", "dob")
    def test_continue_btn_inactive_dob_year_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.set_captcha("LESIGH")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.select_year("1980")
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT A CAPTCHA SET
    @attr("join", "functional", "continue_btn", "captcha")
    def test_continue_btn_inactive_captcha_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.click_opt_in_checkbox()
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.set_captcha("LESIGH")
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

    #TEST CONTINUE BUTTON WILL NOT ACTIVATE WITHOUT OPT IN CHECKBOX CHECKED
    @attr("join", "functional", "continue_btn", "optin")
    def test_continue_btn_inactive_optin_none(self):
        jp = self.join_page
        jp.set_email(self.email)
        jp.set_password("qaauto")
        jp.set_zipcode("92131")
        jp.click_male_button()
        jp.select_month("Feb")
        jp.select_day("1")
        jp.select_year("1980")
        jp.set_captcha("LESIGH")
        time.sleep(.5)
        self.assertFalse(jp.continue_button.is_enabled())
        jp.click_continue_button()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join#/")
        jp.click_opt_in_checkbox()
        self.assertTrue(jp.continue_button.is_enabled())
        self.assertTrue(jp.continue_btn_green.is_displayed())

class TestEventfulJoinPageFBSignIn(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.join_page = JoinPage(cls.driver)
        cls.join_page.navigate_to_join_form()
        cls.join_page.get_all_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDown(self):
        self.driver.quit()

    #TEST FACEBOOK SIGNUP WINDOW IS CORRECT WINDOW POPS UP IN NEW WINDOW
    @attr("join", "functional", "facebook", "popup")
    def test_facebook_signin_popup(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        time.sleep(0)
        self.assertEqual(jp.number_of_windows(), 2)
        jp.switch_to_popup_window()
        self.facebook_logo = self.driver.find_element_by_xpath(".//*[@id='homelink']")
        self.assertTrue(self.facebook_logo.is_displayed())
        self.assertEqual(self.driver.title, "Facebook")

    #TEST USER LANDS ON 'BUILD YOUR PROFILE' PAGE AFTER SIGN IN (for user who hasnt done so yet)
    @attr("join", "functional", "facebook")
    def test_facebook_signin_landing_page(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        jp.switch_to_popup_window()
        jp.set_facebook_known_email_pass()
        jp.switch_to_main_window()
        self.wait.until(lambda driver: jp.build_your_profile)
        self.assertEqual(self.driver.title, "Eventful Tracker")
        self.assertEqual(self.driver.current_url, "http://eventful.com/tracker#/")

    #TEST USER IS ACTUALLY SIGNED IN AFTER SIGNING IN & USERNAME/SIGN OUT LINKS DISPLAYED
    @attr("join", "functional", "facebook")
    def test_facebook_signin_success(self):
        jp = self.join_page
        jp.facebook_signup_button.click()
        time.sleep(0)
        jp.switch_to_popup_window()
        jp.set_facebook_known_email_pass()
        jp.switch_to_main_window()
        self.wait.until(lambda driver: jp.build_your_profile)
        self.assertEqual(jp.user_panel.get_attribute('class'), "logged-in")
        self.assertEqual(jp.user_panel_username.get_attribute('class'), "username first")
        self.assertEqual(jp.user_panel_signout.text, "Sign out")

class TestEventfulJoinPageLinks(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(10)
        #cls.wait = WebDriverWait(cls.driver, 10)
        cls.join_page = JoinPage(cls.driver)
        cls.join_page.navigate_to_join_form()
        #cls.join_page.get_all_elements()

    @classmethod
    def tearDown(self):
        self.driver.quit()

    #TEST NAMES & COUNT OF ALL DISPLAYED LINKS ON JOIN PAGE, ASSERT NAMES MATCH & TOTALS MATCH (currently 21 links)
    @attr("join", "links", "ui")
    def test_join_page_all_links_names_count(self):
        jp = self.join_page
        jp.get_all_elements()
        self.assertEqual(jp.all_displayed_page_links(), ['SIGN UP WITH FACEBOOK', 'Not in the US?', 'Terms of Use', 'Privacy Policy',
                                                         'Video Services Policy', 'Sign In', 'Sign Up', 'About', 'Blog', 'FAQ',
                                                         'Advertise', 'Data Licensing', 'Jobs', 'Developer API', 'Privacy Policy',
                                                         'Your California Privacy Rights', 'Terms of Use', 'Ad Choices',
                                                         'Mobile User Agreement', 'Contact Us', 'Video Services Policy'])
        self.assertEqual(len(jp.all_displayed_page_links()), 21)


    #TEST LINK IS GOOD - FACBOOK SIGN UP, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_facebook_signup(self):
        jp = self.join_page
        jp.get_header_elements()
        jp.facebook_signup_button.click()
        time.sleep(0)
        self.assertEqual(jp.number_of_windows(), 2)
        jp.switch_to_popup_window()
        self.facebook_logo = self.driver.find_element_by_xpath(".//*[@id='homelink']")
        self.assertTrue(self.facebook_logo.is_displayed())
        self.assertEqual(self.driver.title, "Facebook")

    #TEST LINK IS GOOD - NOT IN THE US LINK, ASSERT "IN THE US?" LINK, CITY AND COUNTRY FIELDS DISPLAYED
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_not_in_us(self):
        jp = self.join_page
        jp.get_form_elements()
        jp.not_in_us_link.click()
        self.assertTrue(jp.in_the_us_link.is_displayed())
        self.assertTrue(jp.city_field.is_displayed())
        self.assertTrue(jp.country_dropdown.is_displayed())

    #TEST LINK IS GOOD - TERMS OF USE LINK IN OPT IN FIELD, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_opt_in_tou(self):
        jp = self.join_page
        jp.get_sign_up_elements()
        jp.opt_in_tou_link.click()
        self.assertEqual(jp.number_of_windows(), 2)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/terms-of-use/")
        self.assertEqual(self.driver.title, "Terms of Use")

    #TEST LINK IS GOOD - PRIVACY POLICY LINK IN OPT IN FIELD, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_opt_in_pp(self):
        jp = self.join_page
        jp.get_sign_up_elements()
        jp.opt_in_pp_link.click()
        self.assertEqual(jp.number_of_windows(), 2)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/privacy/current.html")
        self.assertEqual(self.driver.title, "Privacy Policy")

    #TEST LINK IS GOOD - VIDEO SERVICES POLICY LINK IN OPT IN FIELD, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_opt_in_vsp(self):
        jp = self.join_page
        jp.get_sign_up_elements()
        jp.opt_in_vsp_link.click()
        self.assertEqual(jp.number_of_windows(), 2)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/privacy/current.html#video-services")
        self.assertEqual(self.driver.title, "Privacy Policy")

    #TEST LINK IS GOOD - EXISTING USER SIGNIN LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_user_signin(self):
        jp = self.join_page
        jp.get_sign_up_elements()
        jp.signin_link.click()
        self.assertEqual(self.driver.current_url, "http://eventful.com/signin")
        self.assertEqual(self.driver.title, "Sign in - Eventful")

    #TEST LINK IS GOOD - PERFORMER SIGNUP LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_performer_signup(self):
        jp = self.join_page
        jp.get_sign_up_elements()
        jp.performer_signup_link.click()
        time.sleep(.5)
        self.assertEqual(self.driver.current_url, "http://eventful.com/join?as=performer#/")
        self.assertEqual(self.driver.title, "Join now - Eventful")

    #TEST LINK IS GOOD - ABOUT LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_about(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[0].click()
        time.sleep(0)
        self.assertEqual(self.driver.current_url, "http://about.eventful.com/")
        self.assertEqual(self.driver.title, "About Eventful, Inc.: Overview")

    #TEST LINK IS GOOD - BLOG LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_blog(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[1].click()
        time.sleep(0)
        self.assertEqual(self.driver.current_url, "http://blog.eventful.com/")
        self.assertEqual(self.driver.title, "Eventful Blog | Concerts + Movies + Events")

    #TEST LINK IS GOOD - FAQ LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_faq(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[2].click()
        time.sleep(0)
        self.assertEqual(self.driver.current_url, "http://support.eventful.com/home")
        self.assertEqual(self.driver.title, "Eventful Support")

    #TEST LINK IS GOOD - ADVERTISE LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_advertise(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[3].click()
        time.sleep(0)
        self.assertEqual(self.driver.current_url, "http://eventful.com/advertise")
        self.assertEqual(self.driver.title, "Events, Concerts, Tickets, Festivals, Kids, Singles, Sports, Music - Eventful")

    #TEST LINK IS GOOD - DATA LICENSING LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_data_licensing(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[4].click()
        time.sleep(0)
        self.assertEqual(self.driver.current_url, "http://eventful.com/licensing")
        self.assertEqual(self.driver.title, "Event Data Licensing - Eventful")

    #TEST LINK IS GOOD - JOBS LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_jobs(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[5].click()
        time.sleep(0)
        self.assertEqual(self.driver.current_url, "http://eventful.com/jobs")
        self.assertEqual(self.driver.title, "Jobs - Eventful")

    #TEST LINK IS GOOD - DEVELOPER API LINK, ASSERT CORRECT WINDOW
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_developer_api(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[6].click()
        time.sleep(0)
        self.assertEqual(self.driver.current_url, "http://api.eventful.com/")
        self.assertEqual(self.driver.title, "Events Feed, Concert & Event API - Eventful API")

    #TEST LINK IS GOOD -PRIVACY POLICY LINK, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_privacy_policy(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[7].click()
        self.assertEqual(jp.number_of_windows(), 2)
        time.sleep(0)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/privacy/current.html")
        self.assertEqual(self.driver.title, "Privacy Policy")

    #TEST LINK IS GOOD - CA PRIVACY POLICY LINK, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_ca_privacy_policy(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[8].click()
        self.assertEqual(jp.number_of_windows(), 2)
        time.sleep(0)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/privacy/current.html#cali-visitors")
        self.assertEqual(self.driver.title, "Privacy Policy")

    #TEST LINK IS GOOD - TERMS OF USE LINK, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_terms_of_use(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[9].click()
        self.assertEqual(jp.number_of_windows(), 2)
        time.sleep(0)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/terms-of-use/")
        self.assertEqual(self.driver.title, "Terms of Use")

    #TEST LINK IS GOOD - AD CHOICES LINK, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_ad_choices(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[10].click()
        self.assertEqual(jp.number_of_windows(), 2)
        time.sleep(0)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/privacy/current.html#onlinead")
        self.assertEqual(self.driver.title, "Privacy Policy")

    #TEST LINK IS GOOD - MOBILE USER AGREEMENT LINK, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_mobile_user(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[11].click()
        self.assertEqual(jp.number_of_windows(), 2)
        time.sleep(0)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/mobile-app-agreement/")
        self.assertEqual(self.driver.title, "Mobile App End User Agreement")

    #TEST LINK IS GOOD - CONTACT US LINK, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_contact_us(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.footer_link_elements_list[12].click()
        time.sleep(0)
        self.assertEqual(self.driver.current_url, "http://about.eventful.com/contact.html")
        self.assertEqual(self.driver.title, "Eventful, Inc.: Contact Us")

    #TEST LINK IS GOOD - VIDEO SERVICES POLICY LINK, ASSERT CORRECT WINDOW & A NEW POPUP
    @attr("join", "links", "ui", "functional")
    def test_join_page_links_video_services(self):
        jp = self.join_page
        jp.get_footer_elements()
        jp.video_services_policy_link.click()
        self.assertEqual(jp.number_of_windows(), 2)
        time.sleep(0)
        jp.switch_to_popup_window()
        self.assertEqual(self.driver.current_url, "http://policies.cbslocal.com/privacy/current.html#video-services")
        self.assertEqual(self.driver.title, "Privacy Policy")

if __name__ == "__main__":
    unittest.main()

