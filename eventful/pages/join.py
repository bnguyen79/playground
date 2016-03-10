import os
import json
import time
from datetime import date
import hashlib
from selenium import selenium
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from pages import BasePage


class JoinPage(BasePage):
    """Eventful Join Page"""

    # url = "http://eventful.com/join"
    join_form_url = "http://www.eventful.com/join"
    performer_join_url = "http://eventful.com/join?as=performer#/"

    def __init__(self, driver):
        super(JoinPage, self).__init__(driver)
        # Page Element Locators
        self.locators = {
            "join_header": {
                "header_logo": (By.ID, "header-logo"),
                "subheader": (By.XPATH, ".//*[@id='content']//h1[text()='Never Miss Events You Love']"),
                "facebook_signup_button": (By.CSS_SELECTOR, "a.facebook"),
                "or_msg": (By.CSS_SELECTOR, ".divider>span"),
                "signup_subheader": (By.CSS_SELECTOR, "h2.join-subhead")
            },
            "join_form": {
                "email_field": (By.ID, "inp-join-email"),
                "password_field": (By.ID, "inp-password1"),
                "zipcode_field": (By.ID, "inp-join-zipcode"),
                "not_in_us_link": (By.XPATH, ".//*[@id='content']/div/div/div/div/form/section[1]/a"),
                "in_the_us_link": (By.XPATH, ".//*[@id='content']/div/div/div/div/form/section[2]/a"),
                "city_field": (By.ID, "inp-mJoin-city"),
                "country_dropdown": (By.ID, "inp-mJoin-country"),
                "male_button": (By.ID, "btn-mJoin-gender-male"),
                "female_button": (By.ID, "btn-mJoin-gender-female"),
                "date_of_birth_msg": (By.CSS_SELECTOR, ".dob-text"),
                "dob_month_dropdown": (By.ID, "dob_month"),
                "dob_day_dropdown": (By.ID, "dob_day"),
                "dob_year_dropdown": (By.ID, "dob_year"),
                "captcha_field": (By.ID, "inp-mJoin-captcha"),
                "continue_button": (By.ID, "inp-join-submit"),
                "opt_in_checkbox": (By.CSS_SELECTOR, ".special-offers>label>span"),
                "opt_in": (By.ID, "inp-mJoin-special-offers")
            },
            "join_sign_up": {
                "opt_in_section": (By.CSS_SELECTOR, ".special-offers>label"),
                "opt_in_tou_link": (By.XPATH, ".//*[@id='content']//label/a[text()='Terms of Use']"),
                "opt_in_pp_link": (By.XPATH, ".//*[@id='content']//label/a[text()='Privacy Policy']"),
                "opt_in_vsp_link": (By.XPATH, ".//*[@id='content']//label/a[text()='Video Services Policy']"),
                "signin_msg": (By.XPATH, "//p[@class='signin-link' and contains(text(),'Already have an account?')]"),
                "signin_link": (By.CSS_SELECTOR, "a#user-join"),
                "performer_signup_msg": (By.XPATH, "//p[@class='signin-link' and contains(text(),'Are you a performer?')]"),
                "performer_signup_link": (By.CSS_SELECTOR, "#performer-join")
            },
            "footer": {
                "footer_links_section": (By.CSS_SELECTOR, "#essentials>ul"),
                "footer_link_elements_list": (By.CSS_SELECTOR, "#essentials ul li"),
                "video_services_policy": (By.CSS_SELECTOR, ".privacy-message-rs"),
                "video_services_policy_link": (By.CSS_SELECTOR, ".privacy-message-rs>a"),
                "footer_logos_list": (By.CSS_SELECTOR, ".footer-logos img"),
                "cbs_local_logo": (By.CSS_SELECTOR, "div.footer-logos img:nth-child(1)"),
                "radiocom_logo": (By.CSS_SELECTOR, "div.footer-logos img:nth-child(2)"),
                "copyright": (By.CSS_SELECTOR, ".footer-copyright")
            },"facebook_header": {
                "header_logo": (By.ID, "header-logo"),
                #"facebook_signup_button": (By.CSS_SELECTOR, "a.facebook"),
                "fb_subheader": (By.XPATH, "//*[@id='content']//h1[contains(text(), 'Complete your facebook profile')]"),
                "subheader_msg_confirm": (By.XPATH, "//ul[@class= 'facebook-requirements']/li[1]"),
                "subheader_msg_enter": (By.XPATH, "//ul[@class= 'facebook-requirements']/li[2]"),
                "subheader_msg_agree": (By.XPATH, "//ul[@class= 'facebook-requirements']/li[3]"),
            },"facebook_join": {
                "email_field": (By.ID, "inp-join-email"),
                "password_field": (By.ID, "inp-password1"),
                "zipcode_field": (By.ID, "inp-join-zipcode"),
                "not_in_us_link": (By.XPATH, ".//*[@id='content']/div/div/div/div/form/section[1]/a"),
                "in_the_us_link": (By.XPATH, ".//*[@id='content']/div/div/div/div/form/section[2]/a"),
                "city_field": (By.ID, "inp-mJoin-city"),
                "country_dropdown": (By.ID, "inp-mJoin-country"),
                "male_button": (By.ID, "btn-mJoin-gender-male"),
                "female_button": (By.ID, "btn-mJoin-gender-female"),
                "date_of_birth_msg": (By.CSS_SELECTOR, ".dob-text"),
                "dob_month_dropdown": (By.ID, "dob_month"),
                "dob_day_dropdown": (By.ID, "dob_day"),
                "dob_year_dropdown": (By.ID, "dob_year"),
                #"captcha_field": (By.ID, "inp-mJoin-captcha"),
                "continue_button": (By.ID, "inp-join-submit"),
                "opt_in_checkbox": (By.CSS_SELECTOR, ".special-offers>label>span"),
                "opt_in": (By.ID, "inp-mJoin-special-offers")
            },"join_success_page":{
                "eventful_logo": (By.XPATH, ".//*[@id='events']/div[1]"),
                "throbber": (By.XPATH, ".//*[@id='throbber']"),
                "thanks_for_joining": (By.XPATH, "//*[@id='events']/h1[text()='Thanks for Joining!']"),
                "joined_successfully": (By.XPATH, ".//*[@id='events']//p[text()='You have successfully joined Eventful. Great events are on the way.']"),
                "change_username_msg": (By.XPATH, ".//*[@id='events']//p[text()='Go to My Eventful Settings at any time to change your username or to add a photo.']"),
                "click_to_continue_link": (By.XPATH, ".//*[@id='events']/p[4]/a"),
                "click_to_continue_msg": (By.XPATH, ".//*[@id='events']/p[4]")
            },"perfomer_sign_up": {
                "performer_signup_subheader": (By.XPATH, "//*[@id='content']//h1[text()='Performer Sign Up']")
            }

        }

        self.page_sections = self.locators.keys()


    def get_header_elements(self):
        self.get_elements(self.locators["join_header"])

    def get_form_elements(self):
        self.get_elements(self.locators["join_form"])

    def get_sign_up_elements(self):
        self.get_elements(self.locators["join_sign_up"])

    def get_footer_elements(self):
        self.get_elements(self.locators["footer"])

        if self.footer_link_elements_list:
            setattr(self, "footer_links", [])
            for link in self.footer_link_elements_list:
                link_set = {}
                link_tag = link.find_element_by_tag_name("a")
                link_url = link_tag.get_attribute("href")
                link_set["text"] = link.text
                link_set["url"] = link_url
                self.footer_links.append(link_set)

    def get_all_elements(self):
        self.get_header_elements()
        self.get_form_elements()
        self.get_sign_up_elements()
        self.get_footer_elements()

    def get_facebook_header(self):
        self.get_elements(self.locators["facebook_header"])

    def get_facebook_join_form(self):
        self.get_elements(self.locators["facebook_join"])

    def get_all_facebook_join_elements(self):
        self.get_facebook_header()
        self.get_facebook_join_form()
        self.get_sign_up_elements()
        self.get_footer_elements()

    def get_performer_sign_up_elements(self):
        self.get_all_elements()
        self.get_elements(self.locators["perfomer_sign_up"])

    def get_join_success_elements(self):
        self.get_elements(self.locators["join_success_page"])

    def valid_email_tld_list(self):
        self.valid_email_tld_list = ["aero","arpa","biz","com","coop","edu","gov","info","int","mil",
                                     "museum","name","net","org","pro","travel","mobi"]
        return self.valid_email_tld_list

    def valid_email_2_character_tld_list(self):
        self.valid_email_2_character_tld_list = ["aa","bb","cc","dd","ab","cd","zz","qq","oo","ii",
                                 "xx","ll","ie","zq","us","at","we"]
        return self.valid_email_2_character_tld_list

    def invalid_email_tld(self):
        self.invalid_email_tld = ["1"," z","a ","a b","   ","123","13","abc123","comm","fart",
                                    "eventful","com!","com?","@com","com@","~com","$com"]      #add more to this list
        return self.invalid_email_tld

    def valid_email_local_list(self):
        self.valid_email_local_list = ["prettyandsimple@example.com","very.common@example.com","disposable.style.email.with+symbol@example.com",
                                       "other.email-with-dash@example.com","^-~~!$%^&*_=+}{'?@eventful.org"]
        return self.valid_email_local_list

    def invalid_email_list(self):
        self.invalid_email_list = ['`#()[]\/|:;"<>,@eventful.org',"Abc.example.com","A@b@c@example.com",'a"b(c)d,e:f;g<h>i[j\k]l@example.com',
                                   'just"not"right@example.com','this\ still not//allowed@example.com','john..doe@example.com',
                                   'john.doe@example..com',"p","!!@","event.com","hot@here","1@1.1","space @here.com"," space @here.com",
                                   'mark`@cbs.com','hash#@cbs.com','paren(@cbs.com','paren)@cbs.com','bracket[@cbs.com','bracket]@cbs.com',
                                   'backslas\h@cbs.com','forwardslash/@cbs.com','line|@cbs.com','colon:@cbs.com','semicolon;@cbs.com',
                                   'quote"@cbs.com','lessthan<@cbs.com','greaterthan>@cbs.com','comma,@cbs.com']
        return self.invalid_email_list

    def known_email_list(self):
        self.known_email_list = ["qa3eventful@outlook.com", "thedariolama@gmail.com", "misslissco@yahoo.com",
                                 "moskunk@gmail.com", "chocolateyes78@hotmail.com", "andrea98us@yahoo.com"]
        return self.known_email_list

    def valid_password_list(self):
        self.valid_password_list = ["ABCDEF","abcdef","abcDEF","123456","abc123","ABC123","123   ","   abc","      ",
                                    "!@#$%^","1234567890!@#$%^&*()1234567890!@#$%^&*()","QWERTYUIOPASDFGHJKLZXCVBNM1234567890qwertyuiopasdfghjklzxcvbnm",
                                    "                                                                            hi"]
        return self.valid_password_list

    def invalid_password_list(self):
        self.invalid_password_list = ["1", "22", "333", "4444", "55555", ""]
        return self.invalid_password_list

    def invalid_zip_list(self):
        self.invalid_zip_list = ["1", "22", "333", "4444"]
        return self.invalid_zip_list

    def invalid_alpha_zipcode_list(self):
        self.invalid_alpha_zipcode_list = ["a", "ab", "abc", "abcd", "ab12"]   #'z z z' works (bug)
        return self.invalid_alpha_zipcode_list

    def unknown_zipcode_list(self):
        self.unknown_zipcode_list = ["00000", "00001", "123456", "abc123"]
        return self.unknown_zipcode_list

    def valid_city_list(self):
        self.valid_city_list = ["Singapore", "Ankara", "Kinshasa", "San Diego", "Paris"]
        return self.valid_city_list

    def invalid_city_list(self):
        self.invalid_city_list = ["ggggg", "92130", "fjfjfj fj"]
        return self.invalid_city_list

    def new_facebook_email(self):
        self.new_facebook_email = "binhtwo_mxggxqt_qa@tfbnw.net"
        return self.new_facebook_email

    @property
    def email_error_msg(self):
        self._email_error_msg = self.driver.find_element_by_css_selector(
            "form[name=joinForm] div:not(.ng-hide).errors-email p#error-mJoin-email-invalidFormat")
        return self._email_error_msg

    @property
    def username_error_msg(self):
        self._username_error_msg = self.driver.find_element_by_css_selector(
            "form[name=joinForm] div:not(.ng-hide).errors-username p#error-mJoin-username-invalidFormat")
        return self._username_error_msg

    @property
    def password_error_msg(self):
        self._password_error_msg = self.driver.find_element_by_css_selector(
            "form[name=joinForm] div:not(.ng-hide).errors-password p#error-mJoin-password-invalidFormat")
        return self._password_error_msg

    @property
    def zipcode_error_msg(self):
        self._zipcode_error_msg = self.driver.find_element_by_css_selector(
            "form[name=joinForm] div:not(.ng-hide).errors-zipcode p#error-mJoin-zipcode-invalidFormat")
        return self._zipcode_error_msg

    @property
    def year_error_msg(self):
        self._year_error_msg = self.driver.find_element_by_css_selector(
            "div.ng-active div p")
        return self._year_error_msg

    @property
    def continue_btn_green(self):
        self._continue_btn_green = self.driver.find_element(By.XPATH, "//*[@id='inp-join-submit' and @class='button lg fixed long submit-btn green']")
        return self._continue_btn_green

    @property
    def captcha_error_msg(self):
        self._captcha_error_msg = self.driver.find_element(By.XPATH, ".//*[@id='error-mJoin-captcha-default']")
        return self._captcha_error_msg

    @property
    def build_your_profile(self):
        self._build_your_profile = self.driver.find_element(By.XPATH, "//div[@id='content']//h1[contains(text(), 'Build Your Profile')]")
        return self._build_your_profile

    @property
    def user_panel(self):
        self._user_panel = self.driver.find_element_by_xpath(".//*[@id='user-panel']")
        return self._user_panel

    @property
    def user_panel_username(self):
        self._user_panel_username = self.driver.find_element_by_xpath(".//*[@id='user-panel']/ul/li[1]")
        return self._user_panel_username

    @property
    def user_panel_signout(self):
        self._user_panel_signout = self.driver.find_element_by_xpath(".//*[@id='user-panel']/ul/li[2]")
        return self._user_panel_signout

    @property
    def underage_error(self):
        self._underage_error = self.driver.find_element(By.XPATH, ".//*[@id='content']/h1")
        return self._underage_error

    @property
    def underage_cookie(self):
        self._underage_cookie = self.driver.find_element(By.XPATH, ".//*[@id='qatools']//td[text()='underage']")
        return self._underage_cookie

    def set_email(self, value):
        self.fill_form_element(self.email_field, value)

    def set_username(self, value):
        self.fill_form_element(self.username_field, value)

    def set_password(self, value):
        self.fill_form_element(self.password_field, value)

    def set_zipcode(self, value):
        self.fill_form_element(self.zipcode_field, value)

    def set_city(self, value):
        self.fill_form_element(self.city_field, value)

    def select_country(self, value):
        self.select_from_dropdown(self.country_dropdown, value)

    def click_male_button(self):
        self.male_button.click()

    def click_female_button(self):
        self.female_button.click()

    def select_month(self, value):
        self.select_from_dropdown(self.dob_month_dropdown, value)

    def select_day(self, value):
        self.select_from_dropdown(self.dob_day_dropdown, value)

    def select_year(self, value):
        self.select_from_dropdown(self.dob_year_dropdown, value)

    def set_captcha(self, value):
        self.fill_form_element(self.captcha_field, value)

    def set_decoded_captcha(self):
        t = int(time.time())
        secret = "purple penguins parading perniciously"
        message = "{}{}".format(t, secret)
        m = hashlib.md5()
        m.update(message)
        hexVal = m.hexdigest()
        self.set_captcha("{}:{}".format(t, hexVal))

    def click_opt_in_checkbox(self):
        self.opt_in_checkbox.click()

    def click_continue_button(self):
        self.continue_button.click()

    def set_email_and_focusout(self, value, sleep=None):
        self.set_form_element_text_and_focusout(self.email_field, value, sleep)

    def set_username_and_focusout(self, value, sleep=None):
        self.set_form_element_text_and_focusout(self.username_field, value, sleep)

    def set_password_and_focusout(self, value, sleep=None):
        self.set_form_element_text_and_focusout(self.password_field, value, sleep)

    def set_zipcode_and_focusout(self, value, sleep=None):
        self.set_form_element_text_and_focusout(self.zipcode_field, value, sleep)

    def set_day_and_focusout(self, value, sleep=None):
        self.set_form_element_text_and_focusout(self.day_field, value, sleep)

    def set_year_and_focusout(self, value, sleep=None):
        self.set_form_element_text_and_focusout(self.year_field, value, sleep)

    def set_facebook_email(self, value):
        self.fb_email = self.driver.find_element(By.XPATH, ".//*[@id='email']")
        self.fill_form_element(self.fb_email, value)

    def set_facebook_pass(self, value):
        self.fb_pass = self.driver.find_element(By.ID, "pass")
        self.fill_form_element(self.fb_pass, value)

    def click_fb_okay_btn(self):
        self.driver.find_element(By.XPATH, "//button[@name= '__CONFIRM__']").click()

    def set_facebook_known_email_pass(self):
        self.fb_email = self.driver.find_element(By.XPATH, ".//*[@id='email']")
        self.fb_pass = self.driver.find_element(By.ID, "pass")
        self.fill_form_element(self.fb_email, "binh_kgoxoli_one@tfbnw.net")
        self.fill_form_element(self.fb_pass, "eventful")
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def set_facebook_new_email_pass(self):
        self.fb_email = self.driver.find_element(By.XPATH, ".//*[@id='email']")
        self.fb_pass = self.driver.find_element(By.ID, "pass")
        self.fill_form_element(self.fb_email, self.new_facebook_email())
        self.fill_form_element(self.fb_pass, "eventful")
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.perform()





