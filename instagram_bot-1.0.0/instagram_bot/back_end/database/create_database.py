#!/usr/bin/python3.8



import sqlite3



def connectToUserDatabase(user_database_address):

    conn = sqlite3.connect(user_database_address)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS followers(
                    links TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS following(
                    links TEXT)''')
    
    conn.close()


def connectToBotActivitiesDatabase(bot_activities_database_address, activities_limit_per_day=None):
    conn = sqlite3.connect(bot_activities_database_address)
    cur  = conn.cursor()

    if activities_limit_per_day:
        cur.execute(f'''CREATE TABLE IF NOT EXISTS insta_temporary_activities(
                        id INTEGER PRIMARY KEY CHECK(id <= {activities_limit_per_day}),
                        activities TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS telegram_button(
                    button TEXT,
                    time TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS insta_permanent_activities(
                    id INTEGER PRIMARY KEY,
                    activities TEXT,
                    time TEXT)''')

    
    conn.close()
