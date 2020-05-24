#!/usr/bin/python3.8



import time, sqlite3, random
from instagram_bot import General, CheckBlock


# این کلاس برای این است که بتوان اشخاصی که صاحب اکانت را آنفالو کرده اند یا اصلا بک نداده اند را پیدا و آنفالو کرد درست مثل یک برنامه آنفالور اینستاگرام روی گوشی های اندروید



class StopTracking:

    def __init__(self, driver, user_database_location, bot_activities_db_address, username):
        self.driver                 = driver
        self.username               = username
        self.user_db_location       = user_database_location
        self.bot_activities_address = bot_activities_db_address
        self.general                = General(self.driver)
        self.connenction            = sqlite3.connect(self.user_db_location)
        self.cursor                 = self.connenction.cursor()

        self.following_button_class = '_5f5mN'
        self.unfollw_option_class   = 'aOOlW'
        self.following_table        = 'following'

    def _goToPersonPage(self, link):
        general_obj = self.general
        general_obj._openPage(link)
    
    def _clickFollowingButton(self, class_name):
        general_obj = self.general
        general_obj._clickClassElement(class_name)
    
    def _clickUnfollowOption(self, class_name):
        general_obj = self.general
        general_obj._clickClassElement(class_name)

    def _unfollowPerson(self, links, number):
        driver                   = self.driver
        user_database_address    = self.user_db_location
        bot_act_db_adress        = self.bot_activities_address
        following_table          = self.following_table
        unfollow_option_element  = self.unfollw_option_class
        following_button_element = self.following_button_class

        for tuple_link in links[0:number]:
            link        = tuple_link[0]
            check_block = CheckBlock(driver, bot_act_db_adress, user_database_address)

            self._goToPersonPage(link)
            self._clickFollowingButton(following_button_element)
            self._clickUnfollowOption(unfollow_option_element)
            check_block._blockDiagnostics(following_table)
            del check_block

    def _getDistinctsLinks(self, number):
        cur = self.cursor
        difference_links = cur.execute('SELECT DISTINCT links FROM following WHERE links Not IN (SELECT DISTINCT links FROM followers)')
        df_links  = difference_links.fetchall()

        if len(df_links) > number:
            return df_links
        return False
    
    def _startUnfollow(self, number_of_unfollow):
        general_obj = self.general
        conn        = self.connenction
        username    = self.username
        links       = self._getDistinctsLinks(number_of_unfollow)

        conn.close()

        if links:
            self._unfollowPerson(links, number_of_unfollow)
            general_obj._openPage("https://www.instagram.com/" + username.lower())
        else:
            general_obj._closeBrowser()
