#!/usr/bin/python3.8

import sqlite3, datetime
from instagram_bot import General


class CheckBlock:

    def __init__(self, driver, bot_activities_address, user_database_location=None):
        self.user_db_location       = user_database_location
        self.bot_activities_address = bot_activities_address

        self.driver      = driver
        self.general     = General(self.driver)

        self.flw_btn_xpth_1 = "/html/body/div[1]/section/main/div/header/section/div[1]/button"
        self.flw_btn_xpth_2 = "/html/body/div[1]/section/main/div/header/section/div[1]/a/button"
        self.flw_btn_xpth_3 = "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button"
        self.flw_btn_xpth_4 = "/html[1]/body[1]/div[1]/section[1]/main[1]/div[1]/header[1]/section[1]/div[1]/div[1]/span[1]/span[1]/button[1]"

        self.block_page_element       = "/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/button[1]"
        self.following_button_element = "//button[contains(text(),'Following')]"
        self.message_button_element   = "//button[contains(text(),'Message')]"

        if self.user_db_location:
            self.connection_a = sqlite3.connect(self.user_db_location)
            self.cursor_a     = self.connection_a.cursor()
        
        self.connection_b = sqlite3.connect(self.bot_activities_address)
        self.cursor_b     = self.connection_b.cursor()

    def _insertToTable(self, current_page=None, table_name=None, activity=None):
        if table_name:
            conn_a = self.connection_a
            cur_a  = self.cursor_a
            cur_a.execute(f'INSERT INTO {table_name} (links) VALUES ("{current_page}")')
            conn_a.commit()
        else:
            try:
                conn_b = self.connection_b
                cur_b  = self.cursor_b
                time   = datetime.datetime.now()
                cur_b.execute(f'INSERT INTO insta_permanent_activities (activities, time) VALUES ("{activity}", "{time}")')
                conn_b.commit()

                #در جدول موقتی فعالیت های ربات وقتی جدول به محدودیت تعریف شده برسد اررو می دهد و دیتابیس را می بندد
                cur_b.execute('INSERT INTO insta_temporary_activities (activities) VALUES ("{activity}")')
                conn_b.commit()
            except sqlite3.IntegrityError:
                user_db_address = self.user_db_location

                if user_db_address:
                    conn_a = self.connection_a
                    conn_a.close()

                conn_b.close()
                
                raise sqlite3.IntegrityError("you have restrictions on registering additional data in the table")

    def _deleteFromTable(self, current_page, table_name):
        conn_a = self.connection_a
        cur_a  = self.cursor_a
        cur_a.execute(f'DELETE FROM {table_name} WHERE links = :links', {'links': current_page})
        conn_a.commit()
    
    def _findMessageButton(self, current_url, xpath_button, table_name=''):
        "وقتی ربات عمل فالو انجام دهد در این متد قبل از اضافه کردن فعالیت به جدول بررسی می شود که آیا دکمه مسیج در پروفایل شخص وجود دارد یا نه"
        general_obj         = self.general
        find_message_button = general_obj._findXpathElement(xpath_button)

        if find_message_button:
            self._insertToTable(current_url, table_name)
            self._insertToTable(activity='follow act')
            return True
        return False

    def _findFollowingButton(self, current_url, xpath_button, table_name=''):
        "وقتی ربات عمل فالو انجام دهد در این متد قبل از اضافه کردن فعالیت به جدول بررسی می شود که آیا دکمه فالویینگ در پروفایل شخص وجود دارد یا نه"
        general_obj           = self.general
        find_following_button = general_obj._findXpathElement(xpath_button)

        if find_following_button:
            self._insertToTable(current_url, table_name)
            self._insertToTable(activity='follow act')
            return True
        return False

    def _findFollowButton(self, current_url, xpath_buttons_flw, table_name=''):
        "وقتی ربات عمل انفالو انجام دهد در این متد بررسی می شود که آیا در پروفایل شخص دکمه فالویینگ به فالو تبدیل شده است یا خیر"
        general_obj = self.general

        for xpath_button_flw in xpath_buttons_flw:
            find_button = general_obj._findXpathElement(xpath_button_flw)

            if find_button:
                self._deleteFromTable(current_url, table_name)
                self._insertToTable(activity='unfollow act')
                return True
        return False

    def _findActionBlockPage(self):
        """در این متد در هر بار فعالیت ربات چک می شود که آیا صفحه اکشن بلاک اینستاگرام وجود دارد یا نه در صورت وجود نداشتن
        true بر می گرداند"""

        general_obj        = self.general
        block_page_element = self.block_page_element
        find_block_page    = general_obj._findXpathElement(block_page_element)

        if not(find_block_page):
            return True
        return False

    def _detectionButton(self, current_url, table_name=''):
        "بررسی می کند که در حال حاضر کدام فعالیت (فالو یا آنفالو و ...) انجام شده است به عبارتی نوع دکمه در پروفایل شخص را بررسی می کند"

        following_button       = self.following_button_element
        message_button_element = self.message_button_element
        follow_buttons         = [self.flw_btn_xpth_1, self.flw_btn_xpth_2, self.flw_btn_xpth_3, self.flw_btn_xpth_4]
        counter                = 0

        while counter < 3:

            if counter == 0:
                find_following_button = self._findFollowingButton(current_url, following_button, table_name)
                if find_following_button:
                    break
            
            elif counter == 1:
                find_message_button = self._findMessageButton(current_url, message_button_element, table_name)
                if find_message_button:
                    break

            elif counter == 2:
                find_follow_and_follow_back_button = self._findFollowButton(current_url, follow_buttons, table_name)
                if find_follow_and_follow_back_button:
                    break

            counter += 1

    def _blockDiagnostics(self, table_name=''):
        "این متد در هر بار فعالیت تشخیص می دهد که شخص بلاک شده است یا خیر"
        general_obj            = self.general
        user_database_address  = self.user_db_location
        current_url_page       = general_obj._getCurrentUrl()
        block_action_page      = self._findActionBlockPage()

        if block_action_page:
            #این شرط زمانی اجرا می شود که ربات صفحه بلاک را پیدا نکرده باشد و در حال لایک کردن پستی باشد
            if ('/tags/' in current_url_page) or ('/p/' in current_url_page):
                self._insertToTable(activity='like act')
                return True
            else:
                self._detectionButton(current_url_page, table_name)
        else:
            general_obj._closeBrowser()
            general_obj._quitBrowser()

        if user_database_address:
            conn_a = self.connection_a
            conn_a.close()
            
        self.connection_b.close()
