#!/usr/bin/python3.8

from instagram_bot import CheckBlock, General
import random



class Popularity:
    
    def __init__(self, driver, user_database_address, bot_activities_address):
        self.driver                 = driver
        self.user_db_location       = user_database_address
        self.bot_activities_address = bot_activities_address

        self.general                = General(self.driver)
        
        # این رنج و محدودیت فالو در واقع برای این است که احتمال بک دادن شخص فالو شده بالا برود
        self.limit_of_follow = random.choice(range(5000, 8000))

        self.follow_button_class      = ['_5f5mN', 'BY3EC']
        self.elemet_amount_popularity = 'g47SY'
        self.following                = 'following'
        self.follow                   = 'Follow'

    def _clickFollowButton(self):
        following_table        = self.following
        driver                 = self.driver
        general_obj            = self.general
        user_db_address        = self.user_db_location
        bot_activities_address = self.bot_activities_address
        button_follow_class    = self.follow_button_class

        for class_name in button_follow_class:
            follow_elm = general_obj._findClassElement(class_name)

            if follow_elm:
                if follow_elm.text == self.follow:
                    check_block_action = CheckBlock(driver, bot_activities_address, user_db_address)
                    general_obj._clickClassElement(class_name)
                    check_block_action._blockDiagnostics(following_table)
                    del check_block_action
                    break
    
    def _differentiateDetection(self, contents):
        #با توجه به محدودیت که برای ربات تعریف شده اگر اختلاف فالور و فالویینگ صفحه شخص کمتر از حد تعریف شده باشد روی دکمه فالو کلیک می شود
        limit_of_follow = self.limit_of_follow

        if (contents[0] - contents[1]) <= limit_of_follow:
            #if (number of followers) - (number of following) <= limit_of_follow
            self._clickFollowButton()

    def _counterPopularity(self):
        "این متد تشخیص می دهد شخصی که قرار است فالو شود چقدر محبوبیت دارد و بعد با توجه به محدودیت مشخص شده تصمیم به فالو می گیرد"
        popularity_elements = self.elemet_amount_popularity
        general_obj         = self.general
        elements            = general_obj._descriptionContents(popularity_elements)
        #elements = [element of posts, element of followers, element of following]

        contents            = []

        contents.append(elements[1].get_attribute('title')) #number of followers as string
        contents.append(elements[2].text) #number of following as string

        for content_str in contents:
            idx = contents.index(content_str)

            if (',' in content_str): #for example content_str is 4,323
                content_str = content_str.replace(',', '')

            number          = int(content_str)
            contents[idx]   = number
        
        self._differentiateDetection(contents)
        #contents = [4323, 8032]
