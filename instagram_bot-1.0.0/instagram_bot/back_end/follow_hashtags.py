#!/usr/bin/python3.8



from instagram_bot import General, CheckBlock, Popularity


class FollowTags:

    def __init__(self, driver, user_database_location, bot_activities_db_address):
        self.like_button_xpath        = "//span[@class='fr66n']//button[contains(@class,'wpO6b')]" #المتت دکمه لایک
        self.liked_button_xpath       = "/html[1]/body[1]/div[1]/section[1]/main[1]/div[1]/div[1]/article[1]/div[2]/section[1]/span[1]/button[1]/*" #المنت دکمه آنلایک
        self.following_hashtag_button = "/html[1]/body[1]/div[1]/section[1]/main[1]/header[1]/div[2]/div[1]/button[1]"
        self.follow_button_xpath_a    = '/html/body/div[1]/section/main/header/div[2]/div[1]/button'
        self.follow_button_xpath_b    = "//div[contains(@class,'bY2yH')]//button[contains(@class,'oW_lN')]"

        self.scroll_window            = 'window.scrollTo(0,document.body.scrollHeight)'
        self.following_button         = "//button[contains(text(),'Following')]"
        self.message_button           = "//button[contains(text(),'Message')]"
        self.page_hashtag             = 'https://www.instagram.com/explore/tags/'
        self.username_person_xpath    = "//a[contains(@class, 'ZIAjV')]"
        self.search_box_xpath         = '//input[@placeholder="Search"]'

        self.list_usernames         = []
        self.user_db_location       = user_database_location
        self.bot_activities_address = bot_activities_db_address
        self.driver                 = driver
        self.general                = General(self.driver)
    
    def _searchHashtags(self, xpath_box, hashtag):
        general_obj = self.general
        box_type    = 'search'
        general_obj._sendValueInBoxByXpath(box_type, xpath_box, hashtag)

    def _getCurrentPageLink(self):
        general_obj      = self.general
        current_url_page = general_obj._getCurrentUrl()
        return current_url_page
    
    def _clickLikeButton(self):
        general_obj        = self.general
        like_button_xpath  = self.like_button_xpath
        liked_button_xpath = self.liked_button_xpath

        find_liked_button = general_obj._findXpathElement(liked_button_xpath)
        aria_label        = find_liked_button.get_attribute('aria-label')

        if aria_label == "Unlike":
            pass
        else:
            general_obj._clickXpathElement(like_button_xpath)
    
    def _goToPersonPage(self):
        general_obj           = self.general
        username_person_xpath = self.username_person_xpath
        follow_button_xpath_b = self.follow_button_xpath_b
        follow_element        = general_obj._findXpathElement(follow_button_xpath_b)
        follow_text           = follow_element.text

        if follow_text == 'Follow':
            username_xpath_element = general_obj._findXpathElement(username_person_xpath)
            username               = username_xpath_element.text

            general_obj._openPage("https://www.instagram.com/" + username + "/")
            return True
        return False

    def _getTagElements(self, tag_name):
        general_obj  = self.general
        tag_elements = general_obj._findTagElements(tag_name)
        return tag_elements
    
    def _clickFollowButton(self, xpath_button):
        general_obj              = self.general
        following_hashtag_button = self.following_hashtag_button
        element_follow           = general_obj._findXpathElement(following_hashtag_button)
        follow_text              = element_follow.text
        
        if follow_text == 'Follow':
            general_obj._clickXpathElement(xpath_button)
    
    def _getUniqLinks(self, persons_link):
        #این متد یک لیست از لینک های یونیک و یکتا را برگشت می دهد
        uniq_links = []
        for person_link in persons_link:
            if person_link not in uniq_links:
                uniq_links.append(person_link)
        
        return uniq_links

    def _openTagPage(self, hashtag):
        if hashtag != '':
            general_obj  = self.general
            hashtags_url = self.page_hashtag
            general_obj._openPage(hashtags_url + hashtag + '/')

    def _checkFollowingButton(self, xpath_flwing):
        general_obj = self.general
        return general_obj._findXpathElement(xpath_flwing)
    
    def _checkMessageButton(self, xpath_button):
        general_obj = self.general
        return general_obj._findXpathElement(xpath_button)
        
    def _detectionDuplicateUsername(self, list_of_usernames):
        # در این متد در هر بار فعالیت بررسی می شود که آیا صفحه ای که ربات قرار است انرا فالو کند در لیست یوزرنیم های ثبت شده در هنگام اجرا این ماژول وجود دارد یا خیر در صورت وجود داشتن کد های مربوط به فالو را اجرا نمی کند در غیر این صورت شخص را فالو می کند و یوزرنیم ان را به لیست یوزرنیم ها اضافه می کند
        driver                 = self.driver
        following_button       = self.following_button
        message_button         = self.message_button
        user_db_address        = self.user_db_location
        bot_activities_address = self.bot_activities_address
        user_page_link         = self._getCurrentPageLink()

        if user_page_link not in list_of_usernames:
            list_of_usernames.append(user_page_link)
            following_button_element = self._checkFollowingButton(following_button)
            message_button_element   = self._checkMessageButton(message_button)
            
            #این شرط برای زمانی است که لیست یوزرنیم ها خالی است و چک می شود که ایا صفحه ای ربات می خواهد فالو کند قبلا توسط ربات یا صاحب اکانت فالو شده است یا خیر در صورت فالو شدن شرط اجرا نمی شود
            if not(following_button_element) and not(message_button_element):
                popularity_counter = Popularity(driver, user_db_address, bot_activities_address)
                popularity_counter._counterPopularity()
                del popularity_counter

    def _followPerson(self, uniq_hrefs, number):
        driver             = self.driver
        general_obj        = self.general
        bot_activities_address = self.bot_activities_address

        for uniq_href in uniq_hrefs[0:number]:
            check_block    = CheckBlock(driver, bot_activities_address)
            usernames_list = self.list_usernames

            general_obj._openPage(uniq_href)
            self._clickLikeButton()
            check_block._blockDiagnostics()
            del check_block

            if self._goToPersonPage():
                self._detectionDuplicateUsername(usernames_list)

    def _getHashtagPostLinksAndFollow(self, number):
        #در صفحه پست های یک هشتگ اسکرول می کند و لینک پست ها را میگیرد و شروع می کند به فالو کردن
        uniq_links   = []
        general_obj  = self.general
        hight_scroll = self.scroll_window

        while len(uniq_links) <= number:
            general_obj._scroll(hight_scroll)
            tag_a_elements_lst = self._getTagElements('a')
            links_lst          = general_obj._getLinks(tag_a_elements_lst, '.com/p/')
            uniq_links         = self._getUniqLinks(links_lst)
        
        self._followPerson(uniq_links, number)
    
    def _openUserPage(self, username):
        general_obj = self.general
        general_obj._openPage("https://www.instagram.com/" + username.lower())

def followHashtags(driver, user_database_location, bot_activities_db_address, username, tags, number_of_follow):
    follow_tags         = FollowTags(driver, user_database_location, bot_activities_db_address)
    follow_button_xpath = follow_tags.follow_button_xpath_a
    search_box_element  = follow_tags.search_box_xpath

    for tag in tags:
        follow_tags._searchHashtags(search_box_element, tag)
        follow_tags._openTagPage(tag)
        follow_tags._clickFollowButton(follow_button_xpath)
        follow_tags._getHashtagPostLinksAndFollow(number_of_follow)
    
    follow_tags._openUserPage(username)

