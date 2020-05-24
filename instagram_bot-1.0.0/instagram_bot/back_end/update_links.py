#!/usr/bin/python3.8

import sqlite3
from instaloader import Instaloader, Profile


#این کلاس در واقع به ما کمک می کند که در هر بار اجرای برنامه لینک فالور ها و فالویینگ های صاحب اکانت را به روز نگه داریم تا بعدا در قسمت های دیگر مثل آنفالو کردن اشخاص به مشکل نخوریم


class UpdateLinks:

    def __init__(self, username, password, database_address):
        self.links_in_tables_of_database = [[], []]
        self.tables_name                 = ['followers', 'following']
        self.temp_list                   = [[], []]

        self.db_address                  = database_address
        self.username                    = username
        self.password                    = password

        self.connenction                 = sqlite3.connect(self.db_address)
        self.cursor                      = self.connenction.cursor()

        self.loader                      = Instaloader()
        self.profile                     = Profile.from_username(self.loader.context, self.username)

    def _submitLoginRequest(self):
        #ارسال درخواست ورود به اکانت اینستاگرام کاربر
        loader   = self.loader
        username = self.username
        password = self.password

        loader.login(username, password)

    def _insertInTable(self, table_name, link):
        cur  = self.cursor
        conn = self.connenction

        cur.execute(f'INSERT INTO {table_name} (links) VALUES ("{link}")')
        conn.commit()

    def _deleteFromTable(self, table_name, link):
        cur  = self.cursor
        conn = self.connenction

        cur.execute(f'DELETE FROM {table_name} WHERE links = :links' , {'links':link})
        conn.commit()
    
    def _shellSort(self, links):
        gap = len(links) // 2
        while gap > 0:
            for i in range(gap, len(links)):
                val = links[i]
                j = i
                while (j >= gap) and (links[j - gap] > val):
                    links[j] = links[j - gap]
                    j -= gap
                links[j] = val
            gap //= 2
    
    def _binearySearch(self, links, value, begin, end):
        mid = (begin + end) // 2
        if begin > end:
            return 0
        elif links[mid] == value:
            return value
        elif links[mid] > value:
            return self._binearySearch(links, value, begin, mid - 1)
        elif links[mid] < value:
            return self._binearySearch(links, value, mid + 1, end)
        
    def _editDatabase(self):
        #این متد دیگر بعد از اولین اجرای ربات توسط کاربر اجرا می شود و هر تغییری که در فالورها و فالویینگ های کاربر توسط خوده کابر ایجاد شده باشد را در دیتابیس ذخیره می کند
        tables_name = self.tables_name
        tmp_lst     = self.temp_list
        links       = self.links_in_tables_of_database

        for table_name in tables_name:
            table_idx = tables_name.index(table_name)

            #مرتب سازی با الگوریتم شل سورت برای باینری سرچ
            self._shellSort(links[table_idx])
            self._shellSort(tmp_lst[table_idx])

            for link in links[table_idx]:
                "اگر لینکی که در دیتابیس وحود دارد در لینک های درون صفحه کاربر وجود نداشته باشد از جدول مربوطه در دیتابیس حذف می شود"
                lnk = self._binearySearch(tmp_lst[table_idx], link, 0, len(tmp_lst[table_idx]) - 1)
                if not(lnk):
                    self._deleteFromTable(table_name, link)

            for tmp_link in tmp_lst[table_idx]:
                "اگر لینکی که در صفحه کاربر وجود دارد در دیتابیس وجود نداشته باشد آنرا به جدول مربوطه در دیتابیس اضافه می کند"
                tmp_lnk = self._binearySearch(links[table_idx], tmp_link, 0, len(links[table_idx]) - 1)
                if not(tmp_lnk):
                    self._insertInTable(table_name, tmp_link)
    
    def _insertInTables(self):
        tmp_links = self.temp_list # temp_links     = [[links of followers], [links of following]]
        tables_name = self.tables_name #tables_name = ["followers", "following"]

        for table_name in tables_name:
            item = tables_name.index(table_name)

            for tmp_link in tmp_links[item]:
                self._insertInTable(table_name, tmp_link)


    def _getFollowersAndFollowing(self):
        # این متد لینک های فالورها و فالویینگ های موجود در صفحه صاحب اکانت را میگیرد و در یک لیست ذخیره می کند
        tmp_lst = self.temp_list
        profile = self.profile

        self._submitLoginRequest()

        for follower in profile.get_followers():
            follower_username = follower.username
            link              = 'https://www.instagram.com/' + follower_username + "/"

            tmp_lst[0].append(link)

        for following in profile.get_followees():
            following_username = following.username
            link               = 'https://www.instagram.com/' + following_username + "/"

            tmp_lst[1].append(link)

    def _getLinksFromDatabase(self):
        #این متد لینک های ذخیره شده در جداول فالور و فالویینگ را میگیرد و یک لیست را بازگشت می دهد
        item         = 0
        links        = self.links_in_tables_of_database
        tables_name  = self.tables_name
        cursor       = self.cursor

        for table_name in tables_name:
            tuple_links = cursor.execute('SELECT * FROM {}'.format(table_name))
            links[item] = [tuple_link[0] for tuple_link in tuple_links]
            item += 1
        
        return links



def updateLinks(username, password, database_address):
    update_links            = UpdateLinks(username, password, database_address)
    conn                    = update_links.connenction
    links                   = update_links._getLinksFromDatabase()
    len_links_of_followers  = len(links[0])
    len_links_of_following  = len(links[1])

    #این شرط برای زمانی است که ربات برای اولین بار توسط کاربر اجرا می شود و دیتابیس مربوطه خالی است
    if (len_links_of_followers == 0) and (len_links_of_following == 0):
        update_links._getFollowersAndFollowing()
        update_links._insertInTables()
    else:
        update_links._getFollowersAndFollowing()
        update_links._editDatabase()

    conn.close()


