# -*- coding: utf-8 -*-
import json
import time
import datetime
from datetime import date
import random
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from nose.tools import *
from nose.plugins.attrib import attr
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.demand_it import DemandIt

class TestEventfulDemandItPageElements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        # self.driver = webdriver.Remote(
        #     command_executor='http://prds-selenium02.jfk.ad.radio.com:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME
        # )
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 20)
        cls.demand_page = DemandIt(cls.driver)
        cls.demand_page.navigate_to_demand_it_page()
        cls.demand_page.get_all_demand_it_page_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    #TEST DEMAND IT MAIN PAGE HAS CORRECT TITLE
    @attr("demand", "title")
    def test_01_demand_it_page_title(self):
        self.assertEqual(self.demand_page.title, "Demand it! - Demand Today's Hottest Artists In Your Local Venue - Eventful")

    #TEST DEMAND IT MAIN PAGE HAS CORRECT URL
    @attr("demand", "url")
    def test_02_demand_it_page_url(self):
        self.assertEqual(self.demand_page.current_url, "http://eventful.com/demand/hottest")

    #TEST DEMAND IT MAIN PAGE ELEMENTS DISLAYED & CORRECT NUMBER OF ITEMS DISPLAYED
    @attr("demand", "ui")
    def test_03_demand_it_all_main_page_elements_displayed(self):
        dip = self.demand_page
        self.assertTrue(dip.sub_demand_campaigns_link.is_displayed())
        self.assertTrue(dip.sub_demand_top_local_link.is_displayed())
        self.assertTrue(dip.sub_demand_top_50_link.is_displayed())
        self.assertTrue(dip.breadcrumbs.is_displayed())
        self.assertTrue(dip.breadcrumbs_home.is_displayed())
        self.assertTrue(dip.breadcrumbs_demand.is_displayed())
        self.assertTrue(dip.demand_it_chart_header.is_displayed())
        self.assertTrue(dip.demand_it_no_1.is_displayed())
        for item in dip.demand_it_rankings_list:
            self.assertTrue(item.is_displayed())
        for item in dip.demand_it_images_list:
            self.assertTrue(item.is_displayed())
        for item in dip.demand_it_title_list:
            self.assertTrue(item.is_displayed())
        for item in dip.demand_it_description_list:
            self.assertTrue(item.is_displayed())
        for item in dip.demand_it_demand_it_count_list:
            self.assertTrue(item.is_displayed())
        for item in dip.demand_it_demand_it_button_list:
            self.assertTrue(item.is_displayed())
        for item in dip.demanded_in_header_list:
            self.assertTrue(item.is_displayed())
        for item in dip.demanded_in_see_all_list:
            self.assertTrue(item.is_displayed())
        for item in dip.demanded_in_cities_list:
            self.assertTrue(item.is_displayed())
        self.assertTrue(dip.what_is_demand_header.is_displayed())
        self.assertTrue(dip.what_is_demand_1.is_displayed())
        self.assertTrue(dip.what_is_demand_1_desc.is_displayed())
        self.assertTrue(dip.what_is_demand_2.is_displayed())
        self.assertTrue(dip.what_is_demand_2_desc.is_displayed())
        self.assertTrue(dip.what_is_demand_3.is_displayed())
        self.assertTrue(dip.what_is_demand_3_desc.is_displayed())
        self.assertTrue(dip.demand_your_performer.is_displayed())
        self.assertTrue(dip.demand_your_performer_field.is_displayed())
        self.assertTrue(dip.demand_your_performer_demand_button.is_displayed())
        self.assertTrue(dip.most_demanding_header.is_displayed())
        self.assertTrue(dip.most_demanding_colleges_header.is_displayed())
        for item in dip.most_demanding_colleges_list:
            self.assertTrue(item.is_displayed())
        self.assertTrue(dip.most_demanding_cities_header.is_displayed())
        for item in dip.most_demanding_cities_list:
            self.assertTrue(item.is_displayed())
        self.assertTrue(dip.not_finding_it.is_displayed())
        self.assertTrue(dip.add_a_demand_icon.is_displayed())
        self.assertTrue(dip.add_a_demand_link.is_displayed())

    #TEST BREADCRUMBS DISPLAYED CORRECTLY
    @attr("demand", "ui", "breadcrumbs")
    def test_04_demand_it_breadcrumbs_contain_correct_text(self):
        dip = self.demand_page
        self.assertEqual(dip.breadcrumbs.text, "Home > Demand > Today's hottest demands")

    #TEST THERE ARE 40 RANKINGS DISPLAYED & RANKS DISPLAYED IN ORDER FROM 1-40
    @attr("demand", "ui", "rankings")
    def test_05_40_demand_rankings_displayed(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demand_it_rankings_list), 40)
        count = 1
        for rank in dip.demand_it_rankings_list:
            self.assertEqual(str(count), rank.text)
            count += 1

    #TEST THERE ARE 40 DEMAND IMAGES DISPLAYED & IMAGES ARE FROM OUR SERVERS
    @attr("demand", "ui", "images")
    def test_06_40_demand_images_displayed(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demand_it_images_list), 40)
        for image in dip.demand_it_images_list:
            self.assertIn("evcdn.com/images/block", image.get_attribute('src'))

    #TEST THERE ARE 40 DEMAND TITLES DISPLAYED & EACH DISPLAYED TITLE MATCHES LINK TITLE & LINK TITLES ARE CORRECT
    @attr("demand", "ui", "titles")
    def test_07_40_demand_titles_displayed(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demand_it_title_list), 40)
        for title in dip.demand_it_title_list:
            self.assertIn(title.text, title.get_attribute('title'))
            self.assertEqual(title.get_attribute('title'), "{} tickets & tour dates".format(title.text))

    #TEST ALL DISPLAYED IMAGE TITLES MATCH DEMAND TITLES
    @attr("demand", "ui", "titles", "images")
    def test_08_demand_image_titles_and_demand_titles_match(self):
        dip = self.demand_page
        image_list = [i.get_attribute('title') for i in dip.demand_it_images_list]
        title_list = [i.text for i in dip.demand_it_title_list]
        self.assertListEqual(image_list, title_list)

    #TEST ALL IMAGE LINKS AND DEMAND TITLE LINKS MATCH
    @attr("demand", "ui", "titles", "images", "links")
    def test_09_demand_image_links_and_demand_title_links_match(self):
        dip = self.demand_page
        image_links = [i.get_attribute('href') for i in dip.demand_it_images_links_list]
        title_links = [i.get_attribute('href') for i in dip.demand_it_title_list]
        self.assertListEqual(image_links, title_links
                             )
    #TEST THERE ARE 40 DEMAND DESCRIPTIONS DISPLAYED
    @attr("demand", "ui", "descriptions")
    def test_10_40_demand_descriptions_displayed(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demand_it_description_list), 40)

    #TEST THERE ARE 40 DEMAND IT COUNTS DISPLAYED & DISPLAYS TEXT 'people'
    @attr("demand", "ui", "counts")
    def test_11_40_demand_counts_displayed(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demand_it_demand_it_count_list), 40)
        for count in dip.demand_it_demand_it_count_list:
            self.assertIn("people", count.text)

    #TEST THERE ARE 40 DEMAND IT BUTTONS DISPLAYED
    @attr("demand", "ui", "buttons")
    def test_12_40_demand_it_buttons_displayed(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demand_it_demand_it_button_list), 40)
        for button in dip.demand_it_demand_it_button_list:
            self.assertEqual(button.text, "Demand it!")

    #TEST THE DEMAND IT COUNT LINKS MATCH THE DEMAND IT BUTTONS LINKS
    @attr("demand", "ui", "counts", "buttons", "links")
    def test_13_demand_counts_links_and_buttons_links_match(self):
        dip = self.demand_page
        count_links = [i.get_attribute('href') for i in dip.demand_it_demand_it_count_list]
        button_links = [i.get_attribute('href') for i in dip.demand_it_demand_it_button_list]
        self.assertListEqual(count_links, button_links)

    #TEST THE DEMAND IT BUTTONS LINKS MATCH DEMAND SUBJECT
    @attr("demand", "ui", "buttons", "links")
    def test_14_demand_it_button_links_match_demand_titles(self):
        dip = self.demand_page
        button_link_title_list = [i.get_attribute('title').encode('utf-8') for i in dip.demand_it_demand_it_button_list]
        demand_title_list = []
        for demand_title in dip.demand_it_title_list:
            demand_title_list.append("Demand {} come to your city!".format(demand_title.text.encode('utf-8')))
        self.assertListEqual(demand_title_list, button_link_title_list)

    #TEST THERE ARE 40 DEMANDED IN HEADERS DISPLAYED
    @attr("demand", "ui",)
    def test_15_40_demanded_in_headers_displayed(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demanded_in_header_list), 40)
        for demand_header in dip.demanded_in_header_list:
            self.assertEqual(demand_header.text, "Demanded in ... See all")

    #TEST THERE ARE 40 DEMANDED IN SEE ALL LINKS DISPLAYED
    @attr("demand", "ui")
    def test_16_40_demanded_in_see_all_links_deserved(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demanded_in_see_all_list), 40)

    #TEST THE 'SEE ALL' LINKS MATCH THE DEMAND TITLES
    @attr("demand", "ui", "links")
    def test_17_demanded_in_see_all_links_match_demand_titles(self):
        dip = self.demand_page
        demand_title_list = []
        see_all_links_list = [i.get_attribute('title').encode('utf-8') for i in dip.demanded_in_see_all_list]
        for demand_title in dip.demand_it_title_list:
            demand_title_list.append("See all {} Demands".format(demand_title.text.encode('utf-8')))
        self.assertListEqual(demand_title_list, see_all_links_list)

    #TEST THERE ARE 80 CITIES LISTS DISPLAYED (2 PER DEMAND)
    @attr("demand", "ui", "cities")
    def test_18_80_demanded_in_cities_lists_displayed(self):
        dip = self.demand_page
        self.assertEqual(len(dip.demanded_in_cities_list), 80)

    """cant figure this out.
    #TEST THERE ARE 6 CITIES PER DEMAND (6 CITIES x 40 DEMANDS)
    def test_19_6_cities_listed_per_demand(self):
        dip = self.demand_page
        self.assertTrue(3*len(dip.demanded_in_cities_list) == len(dip.demanded_in_cities_links_list))
        for list in dip.demanded_in_cities_list:
            city_list = []
            city_list.append(list.text)
            #self.assertEqual(len(city_list), 3)
            print list.get_attribute('href')
    """

    #TEST WHAT IS DEMAND SECTION NUMBERS ARE DISPLAYED IN CORRECT ORDER
    @attr("demand", "ui")
    def test_19_what_is_demand_number_order(self):
        dip = self.demand_page
        self.assertEqual(dip.what_is_demand_1.text, "1")
        self.assertEqual(dip.what_is_demand_2.text, "2")
        self.assertEqual(dip.what_is_demand_3.text, "3")

    #TEST WHAT IS DEMAND SECTION DISPLAYS CORRECT TEXT
    @attr("demand", "ui")
    def test_20_what_is_demand_text(self):
        dip = self.demand_page
        self.assertEqual(dip.what_is_demand_1_desc.text, "Demand that your favorite performers come to your town.")
        self.assertEqual(dip.what_is_demand_2_desc.text, "Spread the word to get your friends and family to join the Demand.")
        self.assertEqual(dip.what_is_demand_3_desc.text, "Eventful will alert you when your events are scheduled.")

    #TEST MOST DEMANDING SECTION, ASSERT THERE ARE 10 LISTINGS IN EACH LIST (COLLEGES, CITIES)
    @attr("demand", "ui")
    def test_21_most_demanding_lists(self):
        dip = self.demand_page
        self.assertEqual(len(dip.most_demanding_colleges_list), 10)
        self.assertEqual(len(dip.most_demanding_cities_list), 10)

    #TEST MOST DEMANDING EACH DISPLAYED LISTING MATCHES LINK - COLLEGES
    @attr("demand", "ui", "links")
    def test_22_most_demanding_links_match_colleges(self):
        dip = self.demand_page
        for listing in dip.most_demanding_colleges_links_list:
            self.assertEqual(listing.get_attribute('title'), "View top demands at {}".format(listing.text))

    #TEST MOST DEMANDING EACH DISPLAYED LISTING MATCHES LINK - CITIES
    @attr("demand", "ui", "links")
    def test_23_most_demanding_link_match_cities(self):
        dip = self.demand_page
        for listing in dip.most_demanding_cities_links_list:
            self.assertEqual(listing.get_attribute('title'), "View top demands in {}".format(listing.text))

    #TEST ADD A DEMAND LINK
    @attr("demand", "ui", "links")
    def test_24_add_a_demand_link(self):
        dip = self.demand_page
        self.assertEqual(dip.add_a_demand_link.get_attribute('href'), "http://eventful.com/demands/new")

    #TEST BREADCRUMBS LINKS
    @attr("demand", "ui", "breadcrumbs")
    def test_25_breadcrumbs_links(self):
        dip = self.demand_page
        self.assertEqual(dip.breadcrumbs_home.get_attribute('href'), "http://sandiego.eventful.com/events")
        self.assertEqual(dip.breadcrumbs_demand.get_attribute('href'), "http://eventful.com/demand")

    #TEST DEMAND YOUR PERFORMER FIELD CONTAINS "start typing a performer" TEXT
    @attr("demand", "ui")
    def test_26_demand_your_performer_field_contains_correct_text(self):
        dip = self.demand_page
        self.assertEqual(dip.demand_your_performer_field.get_attribute('class'), 'inactive')
        self.assertEqual(dip.demand_your_performer_field.get_attribute('alt'), "start typing a performer")

class TestEventfulDemandItDemandYourFavoritePerformer(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Firefox()
        # self.driver = webdriver.Remote(
        #     command_executor='http://prds-selenium02.jfk.ad.radio.com:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME
        # )
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 20)
        cls.demand_page = DemandIt(cls.driver)
        cls.demand_page.navigate_to_demand_it_page()
        cls.demand_page.get_demand_it_right_column_what_is_elements()
        cls.now = datetime.datetime.now().strftime("%Y%m%d%H%M")
        cls.email = "qa3eventful+{}@outlook.com".format(cls.now)
        cls.username = "qa3eventful{}".format(cls.now)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()

    #TEST DEAFULT FIELD TEXT GOES AWAY WHEN FIELD FOCUSED ON, ASSERT TEXT IS DISPLAYED BEFORE & GONE AFTER FOCUS
    @attr("demand", "ui")
    def test_01_field_text_goes_away_when_focused(self):
        dip = self.demand_page
        self.assertEqual(dip.demand_your_performer_field.get_attribute('class'), "inactive")
        dip.click_demand_your_perfomer_field()
        self.assertEqual(dip.demand_your_performer_field.get_attribute('class'), "")

    #TEST FIELD TYPEAHEAD DOESNT APPEAR ON FIRST CHARACTER INPUT
    @attr("demand", "ui", "typeahead")
    def test_02_typeahead_doesnt_appear_on_1st_character(self):
        dip = self.demand_page
        for item in dip.typeahead_1_character_list():
            dip.set_demand_your_performer(item)
            time.sleep(1)
            self.assertEqual(dip.typeahead_popover, "display: none;")

    #TEST FIELD TYPEAHEAD LOADING SYMBOL DISPLAYS
    @attr("demand", "ui", "typeahead")
    def test_03_typeahead_loading_symbol_displays(self):
        dip = self.demand_page
        dip.set_demand_your_performer("beyonce")
        self.assertEqual(dip.typeahead_loading_symbol, "type-ahead loading")

    #TEST FIELD TYPEAHEAD APPEARS ON 2ND CHARACTER
    @attr("demand", "ui", "typeahead")
    def test_04_typeahead_loads_on_2nd_character(self):
        dip = self.demand_page
        for item in dip.typeahead_2_character_list():
            dip.set_demand_your_performer(item)
            print "Testing - {}".format(item)
            dip.wait_until_visible(dip.demand_your_performer_typeahead)
            #time.sleep(1)
            self.assertEqual(dip.typeahead_popover, "display: block;")
            self.assertTrue(dip.demand_your_performer_typeahead.is_displayed())

    #TEST TYPEAHEAD DISPLAYS CORRECT NUMBER OF RESULTS - 10 MAX
    @attr("demand", "ui", "typeahead")
    def test_05_typeahead_displays_10_results_max(self):
        dip = self.demand_page
        for item in dip.demand_performers_list():
            dip.set_demand_your_performer(item)
            print "Testing - {}".format(item)
            dip.wait_until_visible(dip.demand_your_performer_typeahead)
            num_of_results = len(dip.demand_your_performer_typeahead_list)
            self.assertTrue(num_of_results <= 11)

    #TEST EACH TYPEAHEAD POPOVER INCLUDES "I can't find my performer - Add them!"
    @attr("demand", "ui", "typeahead")
    def test_06_typeahead_results_include_cant_find(self):
        dip = self.demand_page
        for item in dip.demand_performers_list():
            dip.set_demand_your_performer(item)
            print "Testing - {}".format(item)
            dip.wait_until_visible(dip.demand_your_performer_typeahead)
            self.assertNotIn("I can't find my performer - Add them!", dip.demand_your_performer_typeahead.text)

    #TEST TYPEAHEAD RESULTS ARE UPDATED WITH EACH CHARACTER THAT THE USER ENTERS
    @attr("demand", "ui", "typeahead")
    def test_07_typeahead_results_updates_with_each_new_character(self):
        dip = self.demand_page
        dip.set_demand_your_performer("or")
        dip.wait_until_visible(dip.demand_your_performer_typeahead)
        first_results = [i.text for i in dip.demand_your_performer_typeahead_list]

        dip.demand_your_performer_field.send_keys("a")
        time.sleep(1)
        second_results = [i.text for i in dip.demand_your_performer_typeahead_list]
        self.assertNotEqual(first_results, second_results)

        dip.demand_your_performer_field.send_keys("n")
        time.sleep(1)
        third_results = [i.text for i in dip.demand_your_performer_typeahead_list]
        self.assertNotEqual(second_results, third_results)
        self.assertNotEqual(first_results, third_results)

    #TEST FIRST TYPEAHEAD RESULT IS HIGHLIGHTED BY DEFAULT
    @attr("demand", "ui", "typeahead")
    def test_08_first_typeahead_result_highlghted_by_default(self):
        dip = self.demand_page
        for item in dip.demand_performers_list():
            dip.set_demand_your_performer(item)
            dip.wait_until_visible(dip.demand_your_performer_typeahead)
            first_performer = dip.demand_your_performer_typeahead_list[0].get_attribute('class')
            self.assertIn("highlight", first_performer)

    #TEST LAST TYPEAHEAD RESULT IS ALWAYS 'I can't find my performer - Add them!'
    @attr("demand", "ui", "typeahead")
    def test_09_last_typeahead_result_is_cant_find(self):
        dip = self.demand_page
        for item in dip.demand_performers_list():
            dip.set_demand_your_performer(item)
            dip.wait_until_visible(dip.demand_your_performer_typeahead)
            num_of_results = len(dip.demand_your_performer_typeahead_list)
            position_of_cant_find = dip.demand_your_performer_typeahead_list.index(dip.cant_find_performer_typeahead_result)+1
            print num_of_results
            print position_of_cant_find
            self.assertTrue(num_of_results == position_of_cant_find)

    #TEST HOVER ACTION OVER TYPEAHEAD, ASSERT HIGHLIGHT STARTING WITH 2nd ITEM SINCE 1st IS HIGHLIGHTED BY DEFAULT
    @attr("demand", "ui", "typeahead")
    def test_10_mouse_hover_highlights_typeahead_selection(self):
        dip = self.demand_page
        for performer in dip.demand_performers_list():
            dip.set_demand_your_performer(performer)
            print "TESTING - {}".format(performer)
            dip.wait_until_visible(dip.demand_your_performer_typeahead)
            for item in dip.demand_your_performer_typeahead_list[1:]:
                self.assertNotIn("highlight", item.get_attribute('class'))
                dip.hover_over(item, .25)
                self.assertIn("highlight", item.get_attribute('class'))

    #TEST THE LETTERS TYPED IN ARE ALSO BOLDED IN TYPEAHEAD RESULTS
    @attr("demand", "ui", "typeahead")
    def test_11_typeahead_results_have_search_characters_bolded(self):
        dip = self.demand_page
        for performer in dip.demand_performers_list():
            dip.set_demand_your_performer(performer)
            dip.wait_until_visible(dip.demand_your_performer_typeahead)
            for item in dip.bold_characters_in_typeahead:
                search_text = dip.demand_your_performer_field.get_attribute('value')
                bold_characters = item.text
                self.assertIn(bold_characters.lower(), search_text.lower())

    #TEST TYPEAHEAD POPOVER GOES AWAY WHEN USER CLICKS ON PERFORMER
    @attr("demand", "ui", "typeahead")
    def test_12_typeahead_goes_away_once_performer_chosen(self):
        dip = self.demand_page
        for performer in dip.demand_performers_list():
            dip.set_demand_your_performer(performer)
            dip.wait_until_visible(dip.demand_your_performer_typeahead)
            self.assertEqual(dip.typeahead_popover, "display: block;")
            dip.click_random_performer_typeahead()
            self.assertEqual(dip.typeahead_popover, "display: none;")

    #TEST TYPEAHEAD SELECTION CLICKED ON IS WHAT POPULATES DEMAND FIELD
    def test_13_demand_field_displays_typeahead_selection_clicked(self):
        dip = self.demand_page
        dip.set_demand_your_performer("lion")
        dip.wait_until_visible(dip.demand_your_performer_typeahead)
        performers_len = len(dip.demand_your_performer_typeahead_list)
        index = random.choice(range(0,performers_len-1))
        parent = dip.demand_your_performer_typeahead_list[index]
        child = parent.find_element_by_class_name('diminished')
        performer_selected = parent.text.replace(child.text,'')
        performer_select = performer_selected.rstrip()

        child.click()
        displayed_performer = dip.demand_your_performer_field.get_attribute('value')
        print parent.text
        print '-------'
        print child.text
        print '-------'
        print performer_select
        print '-------'
        print displayed_performer
        print '-------'
        self.assertEqual(performer_selected, displayed_performer)
        """
        text = dip.get_random_performer_typeahead().text
        print text
        dip.demand_your_performer_typeahead_list.index(text).click()
        time.sleep(5)
        """


    #TEST USER CAN SCROLL THRU TYPEAHEAD WITH KEYBOARD
    #TEST SIGN IN/UP POPUP WINDOW APPEARS WHEN "I can't find..." IS SELECTED - NOT SIGNED IN
    #TEST CREATE A PERFORMER POPUP WINDOW APPEARS WHEN "I can't find..." IS SELECTED - SIGNED IN

    """might not test this
    #TEST BACKGROUND COLOR OF HIGHLIGHT
    def test_backgroiund_color(self):
        dip = self.demand_page
        dip.set_demand_your_performer("lion")
        dip.wait_until_visible(dip.demand_your_performer_typeahead)
        performer = dip.demand_your_performer_typeahead_list[4]
        dip.hover_over(performer, 5)

        #color = performer.find_element_by_class_name("click-result result-type-undefined highlight")
        rgb = performer.value_of_css_property('background-color')
        print rgb
    """





    #TEST THESE PAGES SIGNED IN, NOT SIGNED IN, MULTUPLE DEMANDS AS FACEBOOK USER
    #TEST DEMAND FLOW PAGE ELEMENTS
    #TEST DEMAND FLOW PAGE 2 ELEMENTS
    #TEST DEMAND FLOW PAGE 3 ELEMENTS
    #TEST DEMAND FLOW PAGE 3 PREFILLS LOCATION BASED ON ZIP ENTERED ON DEMAND PAGE 2
    #TEST DEMAND IT! CAMPAIGNS PAGE
    #TEST TOP LOCAL DEMANDS PAGE
    #TEST DEMAND IT! TOP 50
    #
    #
    #