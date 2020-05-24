#!/usr/bin/python3.8

import random
from time import sleep
from instagram_bot import login_instagram_page, Keys
import requests
from selenium.common.exceptions import TimeoutException


#این کلاس یک کلاس مهم است زیرا هر عملی که ربات انجام می دهد اعم از فالو, انفالو, گرفتن لینک صفحات و ... توسط این قسمت انجام می شود

class General:

    def __init__(self, driver):
        self.driver = driver
    
    def _sendRequestsForCheckConnection(self, site_url):
        DisconnectionError = requests.exceptions.ConnectionError
        
        try:
            req  = requests.get(site_url)
            return req.status_code
        except DisconnectionError:
            raise DisconnectionError("Internet is not connect")

    def _randomTimeToSleep(self, begin, end):

        begin_number = random.choice(range(begin, end))
        end_number   = random.choice(range(begin, end))

        if (begin_number > end_number):
            begin_number, end_number = end_number, begin_number

        elif (begin_number == end_number):
            end_number += begin_number

        to_sleep     = random.choice(range(begin_number, end_number))

        sleep(to_sleep)

    def _quitBrowser(self):
        driver = self.driver
        driver.quit()

    def _closeBrowser(self):
        driver = self.driver
        driver.close()

    def _getCurrentUrl(self):
        driver = self.driver
        return driver.current_url

    def _openPage(self, page_url):
        driver    = self.driver
        insta_url = "https://instagram.com"
        code      = self._sendRequestsForCheckConnection(insta_url)

        if code == 200:
            try:
                self._randomTimeToSleep(5, 7)
                driver.get(page_url)
                self._randomTimeToSleep(5, 7)
            except TimeoutException:
                pass
        else:
            raise RuntimeError(f"code requests for connection is {str(code)}")

    def _refreshPage(self):
        driver = self.driver
        driver.refresh()
        self._randomTimeToSleep(15, 21)

    def _clickEndKeyboadButton(self, element):
        element.send_keys(Keys.END)
        self._randomTimeToSleep(5, 11)

    def _sendValueInBoxByXpath(self, box_type, xpath_box, value):
        self._randomTimeToSleep(5, 11)

        if (box_type == 'search') or (box_type == "text_box"):
            self._clearXpathElement(xpath_box)
            self._sendKeysToXpathElement(xpath_box, value)
        elif box_type == 'comment':
            self._clearXpathElement(xpath_box)
            self._clickXpathElement(xpath_box)
            self._sendKeysToXpathElement(xpath_box, value)

    def _findXpathElement(self, xpath):
        driver = self.driver
        self._randomTimeToSleep(5, 11)
        try:
            if driver.find_element_by_xpath(xpath):
                self._randomTimeToSleep(10, 16)
                xpath_element = driver.find_element_by_xpath(xpath)
                return xpath_element
        except Exception:
            return False

    def _findClassElement(self, class_name):
        driver = self.driver
        self._randomTimeToSleep(5, 11)
        try:
            if driver.find_element_by_class_name(class_name):
                self._randomTimeToSleep(10, 16)
                class_element = driver.find_element_by_class_name(class_name)
                return class_element
        except Exception:
            return False

    def _findTagElement(self, tag):
        driver = self.driver
        self._randomTimeToSleep(5, 11)
        try:
            if driver.find_element_by_tag_name(tag):
                self._randomTimeToSleep(10, 16)
                tag_element = driver.find_element_by_tag_name(tag)
                return tag_element
        except Exception:
            return False

    def _findCssElement(self, selector):
        driver = self.driver
        self._randomTimeToSleep(5, 11)
        try:
            if driver.find_element_by_css_selector(selector):
                self._randomTimeToSleep(10, 16)
                css_element = driver.find_element_by_css_selector(selector)
                return css_element
        except Exception:
            return False

    def _findClassElements(self, class_name):
        driver = self.driver
        self._randomTimeToSleep(5, 11)
        try:
            if driver.find_elements_by_class_name(class_name):
                self._randomTimeToSleep(10, 16)
                class_elements = driver.find_elements_by_class_name(class_name)
                return class_elements
        except Exception:
            return False

    def _findTagElements(self, tag_name):
        driver = self.driver
        self._randomTimeToSleep(5, 11)
        try:
            if driver.find_elements_by_tag_name(tag_name):
                self._randomTimeToSleep(10, 16)
                tag_elements = driver.find_elements_by_tag_name(tag_name)
                return tag_elements
        except Exception:
            return False

    def _findXpathElements(self, xpath):
        driver = self.driver
        self._randomTimeToSleep(5, 11)
        try:
            if driver.find_elements_by_xpath(xpath):
                self._randomTimeToSleep(10, 16)
                xpath_elements = driver.find_elements_by_xpath(xpath)
                return xpath_elements
        except Exception:
            return False

    def _scroll(self, scroll_type, scroll_class=None):
        driver = self.driver
        self._randomTimeToSleep(15, 21)

        if scroll_class:
            scroll_element = self._findClassElement(scroll_class)
            if scroll_element:
                driver.execute_script(scroll_type, scroll_element)
            else:
                raise TypeError("scroll element of the corresponding page not found")
        else:
            driver.execute_script(scroll_type)

        self._randomTimeToSleep(10, 21)

    def _clickCssSelectorElement(self, css_selector):
        self._randomTimeToSleep(5, 11)
        elemet = self._findCssElement(css_selector)

        if elemet:
            elemet.click()
            self._randomTimeToSleep(35, 51)
        else:
            raise TypeError("no css selector element found for click")

    def _clickXpathElement(self, xpath_button):
        self._randomTimeToSleep(5, 11)
        button_elemet = self._findXpathElement(xpath_button)

        if button_elemet:
            button_elemet.click()
            self._randomTimeToSleep(35, 51)
        else:
            raise TypeError("no xpath element found for click")

    def _clickClassElement(self, class_button):
        self._randomTimeToSleep(5, 11)
        button_elemet = self._findClassElement(class_button)

        if button_elemet:
            button_elemet.click()
            self._randomTimeToSleep(35, 51)
        else:
            raise TypeError("no class element found for click")

    def _clearXpathElement(self, xpath_textbox):
        text_box_element = self._findXpathElement(xpath_textbox)

        if text_box_element:
            text_box_element.clear()
            self._randomTimeToSleep(10, 16)
        else:
            raise TypeError("no xpath element found for clear text box")

    def _sendKeysToXpathElement(self, xpath_box, text):
        box_element = self._findXpathElement(xpath_box)

        if box_element:
            box_element.send_keys(text)
            self._randomTimeToSleep(10, 21)
        else:
            raise TypeError("no xpath element found for send keys to box")

    def _descriptionContents(self, class_name):
        "این متد کانتنت و محتوا صفحه شخص را می گیرد\n\nبه طور مثال:\n\n20 posts  45k followers  4,321 following"
        description_contents = self._findClassElements('g47SY')

        if description_contents:
            return description_contents
        else:
            raise TypeError("we could not find description contents")

    def _getLinks(self, elements, piece_of_link='.com/'):
        links = []
        for element in elements:
            link = element.get_attribute('href')
            if piece_of_link in link:
                links.append(link)
        return links

