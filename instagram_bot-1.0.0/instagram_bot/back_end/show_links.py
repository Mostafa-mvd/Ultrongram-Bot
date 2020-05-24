#!/usr/bin/python3.8

import sqlite3



#این متد در واقع بیشتر برای برنامه نویس ها نوشته شده تا به راحتی به توانند مقادیری که درون دیتابیس ذخیره شده را ببینند ولی می توان از این کلاس برای نشان دادن اشخاصی که صاحب یک اکانت را آنفالو کرده اند یا اصلا بک نداده اند هم استفاده کرد


class ShowLinksFromDataBase:

    def __init__(self, db_address):
        self.message    = "\n\t\t\tthis table is empty\n"
        self.db_address = db_address
        self.connection = sqlite3.connect(self.db_address)
        self.cursor     = self.connection.cursor()

    def _showLinks(self, links):
        if len(links) > 0:
            for tuple_link in links:
                link      = tuple_link[0]
                link_item = links.index(tuple_link) + 1
                yield link_item, link
        else:
            print(self.message)
    
    def _whoUnfollowedYou(self):
        cur   = self.cursor
        links = cur.execute('SELECT DISTINCT links FROM following WHERE links Not IN (SELECT DISTINCT links FROM followers)')
        return links.fetchall()
    
    def _getLinksFromTable(self, table_name=''):
        cur   = self.cursor
        links = cur.execute(f'SELECT * FROM {table_name}')
        return links.fetchall()

    def _getLinksFromDatabase(self, table_name):
        conn = self.connection

        if (table_name):
            tpl_links = self._getLinksFromTable(table_name)
        else:
            tpl_links = self._whoUnfollowedYou()

        conn.close()
        return len(tpl_links), self._showLinks(tpl_links)
