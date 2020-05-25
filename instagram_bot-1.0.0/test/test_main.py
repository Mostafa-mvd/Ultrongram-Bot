#!/usr/bin/python3.8


import unittest
from instagram_bot import users_db_location, activities_db_location
from instagram_bot import InstagramBot, connectToBotActivitiesDatabase
import os
import warnings
import time



def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test



def print_acts(acts_generator):
    for act in acts_generator:
        print(f'{act[0]} - {act[1]}')
    print("\t+++++++++++++++++++++\t")



class TestBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = "vahdanim77"
        cls.password = "Mostafa2019"

        cls.user_database_address = users_db_location + "459185918" + ".db"
        cls.bot_act_db_address    = activities_db_location + "459185918" + "_activities.db"

        connectToBotActivitiesDatabase(cls.bot_act_db_address, activities_limit_per_day=100)
    
    def setUp(self):
        time.sleep(10)

        self.insta_bot = InstagramBot(self.username, self.password, self.user_database_address, self.bot_act_db_address)
    
    def tearDown(self):
        self.insta_bot.driver.close()
    
    def show_links(self):
        bot_acts = self.insta_bot._showLinks(self.bot_act_db_address, "telegram_button")
        acts     = bot_acts[1]
        print_acts(acts)


        bot_acts = self.insta_bot._showLinks(self.bot_act_db_address, "insta_permanent_activities")
        acts     = bot_acts[1]
        print_acts(acts)



        bot_acts = self.insta_bot._showLinks(self.bot_act_db_address, "insta_temporary_activities")
        acts     = bot_acts[1]
        print_acts(acts)


        bot_acts = self.insta_bot._showLinks(self.user_database_address, "followers")
        acts     = bot_acts[1]
        print_acts(acts)



        bot_acts = self.insta_bot._showLinks(self.user_database_address, "following")
        acts     = bot_acts[1]
        print_acts(acts)
    
    @ignore_warnings
    def test_stop_tracking(self):
        self.insta_bot._login()
        self.insta_bot._updateLinks()
        self.insta_bot._stopTracking()

    @ignore_warnings
    def follow(self):
        self.insta_bot._login()
        self.insta_bot._updateLinks()
        self.insta_bot._follow()
    
    @ignore_warnings
    def like_follower(self):
        self.insta_bot._login()
        self.insta_bot._updateLinks()
        self.insta_bot._likeTimeLine()


if __name__ == "__main__":
    unittest.main()


