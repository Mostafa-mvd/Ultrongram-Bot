#!/usr/bin/python3.8


from instagram_bot import Popularity, General


class FollowNames:

	def __init__(self, driver):
		self.scroll_extreme     = 'arguments[0].scrollTo(0,100*document.body.scrollHeight)'
		self.following_button   = "//button[contains(text(),'Following')]"
		self.message_button     = "//button[contains(text(),'Message')]"
		self.search_box_xpath   = '//input[@placeholder="Search"]'
		self.person_links_class = "yCE8d  "
		self.scroll_box         = 'fuqBx'

		self.driver  = driver
		self.general = General(self.driver)

	def _searchName(self, xpath_box, name):
		general_obj = self.general
		box_type    = 'search'
		general_obj._sendValueInBoxByXpath(box_type, xpath_box, name)

	def _extremeScroll(self):
		general_obj    = self.general
		scroll_box     = self.scroll_box
		extreme_scroll = self.scroll_extreme
		general_obj._scroll(extreme_scroll, scroll_box)

	def _getPersonLinks(self):
		general_obj = self.general
		links_class = self.person_links_class
		elements    = general_obj._findClassElements(links_class)
		links       = general_obj._getLinks(elements)
		return links

	def _checkFollowingButton(self, xpath_flwing):
		general_obj = self.general
		return general_obj._findXpathElement(xpath_flwing)

	def _checkMessageButton(self, xpath_button):
		general_obj = self.general
		return general_obj._findXpathElement(xpath_button)

	def _FollowPersonPage(self, lst_links, number, user_db_location, bot_activities_address):
		driver            = self.driver
		general_obj       = self.general
		following_button  = self.following_button
		message_button    = self.message_button

		for link in lst_links[0:number]:
			general_obj._openPage(link)

			flwing_btn_element = self._checkFollowingButton(following_button)
			msg_btn_element    = self._checkMessageButton(message_button)

			if not(flwing_btn_element) and not(msg_btn_element):
				popularity_counter = Popularity(driver, user_db_location, bot_activities_address)
				popularity_counter._counterPopularity()
				del popularity_counter

	def _getCorrectLinks(self, url_of_pages, name):
		#این متد به ربات کمک می کند که تشخیص دهد در باکس سرچ کدام پیشنهاد ها واقعا یوزرنیم است تا بتواند آنها را فالو کند در صورت هشتگ بود یا لوکیشن یک مکان از گرفتن لینک آنها خودداری می کند
		links_lst = []
		for url_of_page in url_of_pages:
			# به عنوان نمونه داریم ['https:' , '' , 'www.instagram.com', 'jashoa_1111' , '']
			pieces_of_link = url_of_page.split('/')
			low_name = name.lower()
			# به عنوان نمونه اگر pieces_of_link[3] is 'jashoa_1111'
			if low_name in pieces_of_link[3]:
				links_lst.append(url_of_page)
		return links_lst
	
	def _openUserPage(self, username):
		general_obj = self.general
		general_obj._openPage("https://www.instagram.com/" + username.lower())


def followNames(driver, names, username, number_of_follow, user_db_address, bot_activities_address):
	follow_names       = FollowNames(driver)
	search_box_element = follow_names.search_box_xpath

	for name in names:
		follow_names._searchName(search_box_element, name)
		follow_names._extremeScroll()

		links         = follow_names._getPersonLinks()
		correct_links = follow_names._getCorrectLinks(links, name)

		follow_names._FollowPersonPage(correct_links, number_of_follow, user_db_address, bot_activities_address)

	follow_names._openUserPage(username)
