#!/usr/bin/python3.8


import sqlite3
from platform import system, architecture
import os
from random import choice
from instagram_bot import (firefox_driver_address_for_linux32, firefox_driver_address_for_linux64, firefox_driver_address_for_windows32, firefox_driver_address_for_windows64, firefox_driver_address_for_mac)
from instagram_bot import (webdriver, activities_db_location, users_db_location)
from instagram_bot import (names_file_address, hashtags_file_address)
from instagram_bot import (ShowLinksFromDataBase, followHashtags, followNames, LikeTimeLine)
from instagram_bot import (updateLinks, connectToUserDatabase, loginToAccaunt, Popularity, StopTracking, getValues)



class InstagramBot:

    opration_system     = system()
    opration_system_bit = architecture()

    def __init__(self, username, password, user_database_address, bot_activities_database_address):
        self.username   = username
        self.password   = password

        self.user_db_address           = user_database_address
        self.bot_activities_db_address = bot_activities_database_address
        self.main_file_location        = os.path.dirname(__file__)

        #در شرط های زیر برنامه تشخیص می دهد که درایور مربوطه را با توجه به نوع سیستم عامل انتخاب کند و در صورت ساخته نشدن درایور ارروی نمایش می دهد

        if (self.opration_system == "Linux") and (self.opration_system_bit[0] == "32bit"):
                self.driver = webdriver.Firefox(executable_path = self.main_file_location + firefox_driver_address_for_linux32)

        elif (self.opration_system == "Linux") and (self.opration_system_bit[0] == "64bit"):
                self.driver = webdriver.Firefox(executable_path = self.main_file_location + firefox_driver_address_for_linux64)

        elif (self.opration_system == "Windows") and (self.opration_system_bit[0] == "32bit"):
            self.driver = webdriver.Firefox(executable_path = self.main_file_location + firefox_driver_address_for_windows32)
        
        elif (self.opration_system == "Windows" and (self.opration_system_bit[0] == "64bit")):
            self.driver = webdriver.Firefox(executable_path = self.main_file_location + firefox_driver_address_for_windows64)

        elif self.opration_system == "Darwin": #Darwin is for mac os
            self.driver = webdriver.Firefox(executable_path = self.main_file_location + firefox_driver_address_for_mac)
    
    def _showLinks(self, database_address, table_name=None):
        user_db_address        = self.user_db_address
        bot_activities_address = self.bot_activities_db_address

        if user_db_address == database_address:
            show_links = ShowLinksFromDataBase(database_address)

        elif bot_activities_address == database_address:
            if table_name:
                show_links = ShowLinksFromDataBase(database_address)
            else:
                raise ValueError("table name parametr is empty")

        else:
            raise ValueError("database not exists")

        links_gener = show_links._getLinksFromDatabase(table_name)

        return links_gener

    def _login(self):
        driver   = self.driver
        username = self.username
        password = self.password

        loginToAccaunt(driver, username, password)

    def _updateLinks(self):
        user_db_address = self.user_db_address
        username        = self.username
        password        = self.password

        connectToUserDatabase(user_db_address)
        updateLinks(username, password, user_db_address)

    def _stopTracking(self):
        user_db_address        = self.user_db_address
        bot_activities_address = self.bot_activities_db_address
        driver                 = self.driver
        username               = self.username

        number_of_unfollow_per_hour = choice(range(7, 11))
        st = StopTracking(driver, user_db_address, bot_activities_address, username)
        st._startUnfollow(number_of_unfollow_per_hour)

    def _follow(self):
        driver                 = self.driver
        user_db_address        = self.user_db_address
        bot_activities_address = self.bot_activities_db_address
        username               = self.username

        random_number               = choice(range(1, 3))
        number_of_follow_per_hour = choice(range(7, 11))

        if random_number == 1:
            hashtag_lst = getValues(hashtags_file_address)
            followHashtags(driver, user_db_address, bot_activities_address, username, hashtag_lst, number_of_follow_per_hour)

        elif random_number == 2:
            username_list = getValues(names_file_address)
            followNames(driver, username_list, username, number_of_follow_per_hour, user_db_address, bot_activities_address)


    def _likeTimeLine(self):
        driver   = self.driver
        username = self.username
        bot_activities_address = self.bot_activities_db_address

        number_of_scroll = choice(range(1, 3))
        #by once scroll get 7 or 8 posts if not liked
        #by twice scroll get 14 or 16 posts if not liked
        like_person = LikeTimeLine(driver, bot_activities_address)
        like_person._goToLikePerson(number_of_scroll, username)





