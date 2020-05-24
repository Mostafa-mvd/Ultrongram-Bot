#!/usr/bin/python3.8


from instagram_bot import General, CheckBlock, Keys
from bs4 import BeautifulSoup


class LikeTimeLine:

    def __init__(self, dirver, bot_activities_address):

        self.driver                 = dirver
        self.bot_activities_address = bot_activities_address
        self.general                = General(self.driver)

        self.like_button_xpath   = "//span[@class='fr66n']//button[contains(@class,'wpO6b')]"
        self.instagram_url       = 'https://www.instagram.com'
        self.body_xpath_element  = "//html//body"
        self.notnow_button_class = 'aOOlW'

    def _openInstagramPage(self):
        general_obj   = self.general
        instagram_url = self.instagram_url

        general_obj._openPage(instagram_url)

    def _clickOnNotnowOption(self):
        general_obj         = self.general
        notnow_button_class = self.notnow_button_class

        general_obj._clickClassElement(notnow_button_class)

    def _clickLikeButton(self):
        general_obj       = self.general
        like_button_xpath = self.like_button_xpath

        general_obj._clickXpathElement(like_button_xpath)
    
    def _goToLikeTimeLine(self, links):
        driver      = self.driver
        general_obj = self.general
        bot_activities_address = self.bot_activities_address

        if len(links) > 0:
            for link in links:
                check_block = CheckBlock(driver, bot_activities_address)
                general_obj._openPage(link)
                self._clickLikeButton()
                check_block._blockDiagnostics()
                del check_block

    def _likeTimeLinePosts(self, number_of_scroll):
        instagram_url = self.instagram_url
        general_obj   = self.general
        driver        = self.driver
        counter       = 0

        posts_link_is_not_liked = []
        body_xpath_element      = self.body_xpath_element

        body_element = general_obj._findXpathElement(body_xpath_element)


        while counter < number_of_scroll:
            general_obj._clickEndKeyboadButton(body_element)
            counter += 1

            page_source  = driver.page_source
            soup         = BeautifulSoup(page_source, 'html.parser')
            article_tags = soup.find_all('article')

            if len(article_tags) > 0:
                for article_tag in article_tags:
                    href_attr = article_tag.find('a', attrs={'class': 'c-Yi7'}).attrs['href']
                    post_link = instagram_url + href_attr
                    svg_tag   = article_tag.find('svg', attrs={'aria-label': 'Like', 'fill': '#262626'})

                    if svg_tag:
                        if post_link not in posts_link_is_not_liked:
                            posts_link_is_not_liked.append(post_link)
            else:
                counter = number_of_scroll
        
        self._goToLikeTimeLine(posts_link_is_not_liked)

    def _goToLikePerson(self, number, username):
        general_obj = self.general

        self._openInstagramPage()
        self._clickOnNotnowOption()
        self._likeTimeLinePosts(number)
        general_obj._openPage("https://www.instagram.com/" + username.lower())
