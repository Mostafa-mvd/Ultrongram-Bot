#!/usr/bin/python3.8


from instagram_bot import login_instagram_page
from instagram_bot import General
import requests


class Login:

    def __init__(self, driver):
        self.driver                 = driver
        self.general_obj            = General(self.driver)
        self.overflow_class         = 'aeJ'
        self.password_textbox_xpath = '//input[@name="password"]'
        self.username_textbox_xpath = '//input[@name="username"]'
        self.login_button_xpath     = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div'

    def _openUserPage(self, url_address):
        general_obj = self.general_obj
        general_obj._openPage(url_address)

    def _openLoginPage(self):
        general_obj = self.general_obj
        general_obj._openPage(login_instagram_page)
    
    def _enterUsername(self, username):
        general_obj            = self.general_obj
        username_textbox_xpath = self.username_textbox_xpath
        general_obj._sendValueInBoxByXpath("text_box", username_textbox_xpath, username)

    def _enterPassword(self, password):
        general_obj            = self.general_obj
        password_textbox_xpath = self.password_textbox_xpath
        general_obj._sendValueInBoxByXpath("text_box", password_textbox_xpath, password)
    
    def _clickLoginButton(self):
        general_obj        = self.general_obj
        login_button_xpath = self.login_button_xpath
        general_obj._clickXpathElement(login_button_xpath)




def loginToAccaunt(driver, username, password):
    login              = Login(driver)
    general_obj        = login.general_obj
    current_url        = login_instagram_page
    repeat             = 0

    login._openLoginPage()

    while (current_url == login_instagram_page):
        code = general_obj._sendRequestsForCheckConnection("https://instagram.com")

        if code == 200:
            if repeat < 2:
                login._enterUsername(username)
                login._enterPassword(password)
                login._clickLoginButton()
                current_url = general_obj._getCurrentUrl()
                repeat += 1
            else:
                raise RuntimeError("username or password is not correct")
        else:
            raise RuntimeError(f"code requests for connection is {str(code)}")
    
    if (len(current_url.split('/')) > 4):
        raise RuntimeError("instagram authentication page")
    else:
        login._openUserPage(current_url + username)
