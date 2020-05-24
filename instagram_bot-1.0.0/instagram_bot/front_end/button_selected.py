#!/usr/bin/python3.8



#این کلاس مربوط به دکمه های شیشه ای ربات تلگرام است و کاربر با انتخاب نوع فعالیت خود مشخص می کند که ربات اینستاگرام چه کاری برایش انجام دهد و همه اررو ها در هنگام اجرای برنامه در این قسمت هندل می شوند تا با توجه به اررو به کابر پیامی نمایش داده شود


#توجه شود که فعالیت های ربات تلگرام و اینستاگرام در دیتابیس های جداگانه ثبت می شوند


from instagram_bot import InvalidSessionIdException, SessionNotCreatedException
from instagram_bot import InteractWithUser
from instagram_bot import InstagramBot, connectToBotActivitiesDatabase
from instagram_bot import users_db_location, activities_db_location
from instagram_bot import get24HourMessage, get7dayMessage, my_bot_token, connection_error_message, successfully_message
from instagram_bot import warning_to_click_unfollow_button, error_txt_file_address, runtime_error_message, login_error_message, warning_to_unfollow_persons, close_driver_error_message, error_message_for_oprating_system, error_message_for_browers
from instagram_bot import ConnectionError, NetworkError, BadRequest

from time import sleep
from datetime import datetime
from random import choice
import sqlite3, requests
from platform import system


class SelectedButtonsHandler:

    def __init__(self, bot, update, users_database_location, activities_db_address):
        self.callback_data ={
                                "_flw":   self._followButton,
                                "_auto":  self._automaticModeButton,
                                "_unflw": self._unfollowButton,
                                "_links": self._showLinksButton
                            }

        self.query         = update.callback_query
        self.data          = self.query.data
        self.bot           = bot
        self.new_time      = datetime.now()
        self.jso           = InteractWithUser.java_script_object
        self.username      = self.jso.username
        self.password      = self.jso.password

        self.datetime_format    = '%Y-%m-%d %H:%M:%S.%f'
        self.user_database_name = str(self.query.message.chat_id) + '.db'
        self.user_db_address    = users_database_location + self.user_database_name
        self.bot_act_db_address = activities_db_address

        self.connection         = sqlite3.connect(self.bot_act_db_address)
        self.cursor = self.connection.cursor()
        
        self.action             = self.cursor.execute('SELECT * FROM telegram_button')
        self.fetch_all          = self.action.fetchall()
        
        self.insta_bot          = InstagramBot(self.username, self.password, self.user_db_address, self.bot_act_db_address)

    def _buttonChoosed(self):
        #در این متد مشخص می شود که که دکمه ای که کاربر انتخاب کرده چه دکمه ای است
        
        callback_data = self.callback_data
        query         = self.query
        data_id       = self.data
        bot           = self.bot

        for button_id, _buttonMethod in callback_data.items():
            if (data_id == button_id):
                return _buttonMethod(bot, query)

    def _followButton(self, bot, query):
        insta_bot          = self.insta_bot
        driver             = insta_bot.driver
        datetime_format    = self.datetime_format
        bot_act_db_address = self.bot_act_db_address
        new_time           = self.new_time
        conn               = self.connection
        cur                = self.cursor
        fetch_all          = self.fetch_all
        chat_id            = query.message.chat_id
        swap               = False
        be_rejected        = True

        #"این شرط برای زمانی است که برای اولین بار روی دکمه فالو زده می شود"
        if len(fetch_all) == 0:
            swap        = True
            be_rejected = False

            #آنفالو باتن در اینجا ذخیره می شود تا بعدا با توجه به فالو باتن و آنفالو باتن ذخیره شده مشخص شود که کاربر در چه زمانی اجازه استفاده از قابلیت آنفالو را دارد

            cur.execute(f'INSERT INTO telegram_button (button, time) VALUES ("unfollow_button", "{new_time}")')
            cur.execute(f'INSERT INTO telegram_button (button, time) VALUES ("follow_button", "{new_time}")')
            conn.commit()
            conn.close()

        #این شرط زمانی اجرا می شود ربات در انجام یک فعالیت به مشکلی خرده باشد این به کاربر اجازه می دهد بدون محدودیت ۲۴ ساعت در صورت وجود اررو دوباره از ربات اجرا بگیرد تا مشخص شود ارور از سمت کاربر رخ داده یا خیر
        elif len(fetch_all) == 1:
            swap = True
        
        #این شرط هم زمانی اجرا می شود که کاربر یک فعالیت را با موفقیت پشت سر گذاشته و بعد از محدودیت ۲۴ ساعت دوباره ربات را فعال کرده است
        elif len(fetch_all) == 2:
            last_run_time = fetch_all[1][1]
            new_strp_time = datetime.strptime(str(new_time), datetime_format)

            previous_run_strp_time = datetime.strptime(str(last_run_time), datetime_format)
            diff_strp_time         = new_strp_time - previous_run_strp_time
            diff_days              = int(diff_strp_time.days)

            if diff_days >= 1:
                last_run    = fetch_all[1][0]
                swap        = True
                be_rejected = False

                cur.execute(f'UPDATE telegram_button SET time="{new_time}" WHERE button="{last_run}"')
                conn.commit()
                conn.close()
            else:
                last_run_strptime = str(previous_run_strp_time).split(' ')[1].split('.')[0]
                passed_time       = str(diff_strp_time).split('.')[0]
                message           = get24HourMessage(last_run_strptime, passed_time)

                bot.send_message(chat_id=chat_id, text=message)
                conn.close()
                driver.close()

        if swap == True:
            number_of_action_per_day = choice(range(130, 200))

            connectToBotActivitiesDatabase(bot_act_db_address, number_of_action_per_day)
            insta_bot._login()
            insta_bot._updateLinks()

            # این شرط زمانی اجرا می شود که  len(fetch_all) == 1 باشد
            if be_rejected:
                cur.execute(f'INSERT INTO telegram_button (button, time) VALUES ("follow_button", "{new_time}")')
                conn.commit()
                conn.close()

            while True:
                insta_bot._follow()
                sleep(3600)


    def _unfollowButton(self, bot, query):
        insta_bot          = self.insta_bot
        driver             = insta_bot.driver
        datetime_format    = self.datetime_format
        new_time           = self.new_time
        conn               = self.connection
        cur                = self.cursor
        fetch_all          = self.fetch_all
        chat_id            = query.message.chat_id
        bot_act_db_address = self.bot_act_db_address

        #کاربر به عنوان اولین فعالیت خود نمی تواند از قابلیت آنفالو ربات استفاده کند و تا زمانی که فعالیت دیگر غیر از  آنفالو انجام ندهد و آنرا تکمیل نکند این شرط برایش اجرا می شود
        if (len(fetch_all) == 0) or (len(fetch_all) == 1):
            bot.send_message(chat_id=chat_id, text=warning_to_click_unfollow_button)
            conn.close()
            driver.close()

        #زمانی که فعالیتی را تکمیل کرده باشد این شرط اجرا می شود
        elif len(fetch_all) == 2:
            # first 1 item is query for follow button or auto button
            last_run_button              = fetch_all[1][0]
            # second 1 item is query for time of follow button or auto button
            time_to_click_last_button    = fetch_all[1][1]
            # first 0 item is query for time of unfollow button and the first 1 item is unfollow button
            time_to_save_unfollow_button = fetch_all[0][1]

            new_strptime       = datetime.strptime(str(new_time), datetime_format)
            previous_strp_time = datetime.strptime(str(time_to_click_last_button), datetime_format)
            unfollow_strp_time = datetime.strptime(str(time_to_save_unfollow_button), datetime_format)

            previous_diff_strp_time = new_strptime - previous_strp_time
            unfollow_diff_strp_time = new_strptime - unfollow_strp_time

            diff_days_pervious = int(previous_diff_strp_time.days)
            diff_days_unfollow = int(unfollow_diff_strp_time.days)

            if diff_days_pervious >= 1:
                if diff_days_unfollow >= 7:
                    number_of_unfollow_per_day = choice(range(130, 200))

                    connectToBotActivitiesDatabase(bot_act_db_address, number_of_unfollow_per_day)
                    insta_bot._login()
                    insta_bot._updateLinks()

                    cur.execute(f'UPDATE telegram_button SET time="{new_time}" WHERE button="unfollow_button"')
                    cur.execute(f'UPDATE telegram_button SET time="{new_time}" WHERE button="{last_run_button}"')
                    conn.commit()
                    conn.close()

                    while True:
                        insta_bot._stopTracking()
                        sleep(3600)
                else:
                    last_run_unfollow_strp_time = str(unfollow_strp_time).split(' ')[1].split('.')[0]
                    passed_time_in_hour         = str(unfollow_diff_strp_time).split('.')[0]

                    message = get7dayMessage(last_run_unfollow_strp_time, diff_days_unfollow, passed_time_in_hour)

                    bot.send_message(chat_id=chat_id, text=message)
                    conn.close()
                    driver.close()
            else:
                last_run_strptime = str(previous_strp_time).split(' ')[1].split('.')[0]
                passed_time       = str(previous_diff_strp_time).split('.')[0]
                message           = get24HourMessage(last_run_strptime, passed_time)

                bot.send_message(chat_id=chat_id, text=message)
                conn.close()
                driver.close()

    def _automaticModeButton(self, bot, query):
        #در قابلیت خودکار کابر می تواند فالو بر اساس هشتگ و فالو بر اساس اسم و لایک کردن اشخاص در تایم لاین را به ربات بسپارد
        
        insta_bot          = self.insta_bot
        driver             = insta_bot.driver
        datetime_format    = self.datetime_format
        new_time           = self.new_time
        conn               = self.connection
        cur                = self.cursor
        fetch_all          = self.fetch_all
        chat_id            = query.message.chat_id
        bot_act_db_address = self.bot_act_db_address
        swap               = False
        be_rejected        = True

        #"این شرط برای زمانی است که برای اولین بار روی دکمه فالو زده می شود"
        if len(fetch_all) == 0:
            swap        = True
            be_rejected = False

            #آنفالو باتن در اینجا ذخیره می شود تا بعدا با توجه به فالو باتن و آئوتو باتن ذخیره شده مشخص شود که کاربر در چه زمانی اجازه استفاده از قابلیت آنفالو را دارد

            cur.execute(f'INSERT INTO telegram_button (button, time) VALUES ("unfollow_button", "{new_time}")')
            cur.execute(f'INSERT INTO telegram_button (button, time) VALUES ("auto_button", "{new_time}")')
            conn.commit()
            conn.close()
            
        #این شرط زمانی اجرا می شود ربات در انجام یک فعالیت به مشکلی خرده باشد این به کاربر اجازه می دهد بدون محدودیت ۲۴ ساعت در صورت وجود اررو دوباره از ربات اجرا بگیرد تا مشخص شود ارور از سمت کاربر رخ داده یا خیر
        elif len(fetch_all) == 1:
            swap = True
        
        #این شرط هم زمانی اجرا می شود که کاربر یک فعالیت را با موفقیت پشت سر گذاشته و بعد از محدودیت ۲۴ ساعت دوباره ربات را فعال کرده است
        elif len(fetch_all) == 2:
            last_run_time          = fetch_all[1][1]
            new_strp_time          = datetime.strptime(str(new_time), datetime_format)
            previous_run_strp_time = datetime.strptime(str(last_run_time), datetime_format)
            diff_strp_time         = new_strp_time - previous_run_strp_time
            diff_days              = int(diff_strp_time.days)

            if diff_days >= 1:
                last_run    = fetch_all[1][0]
                swap        = True
                be_rejected = False

                cur.execute(f'UPDATE telegram_button SET time="{new_time}" WHERE button="{last_run}"')
                conn.commit()
                conn.close()

            else:
                last_run_strptime = str(previous_run_strp_time).split(' ')[1].split('.')[0]
                passed_time       = str(diff_strp_time).split('.')[0]
                message           = get24HourMessage(last_run_strptime, passed_time)

                bot.send_message(chat_id=chat_id, text=message)
                conn.close()
                driver.close()

        if swap == True:
            number_of_action_per_day = choice(range(400, 500))

            connectToBotActivitiesDatabase(bot_act_db_address, number_of_action_per_day)
            insta_bot._login()
            insta_bot._updateLinks()

            # این شرط زمانی اجرا می شود که  len(fetch_all) == 1 باشد
            if be_rejected:
                cur.execute(f'INSERT INTO telegram_button (button, time) VALUES ("auto_button", "{new_time}")')
                conn.commit()
                conn.close()

            while True:
                insta_bot._follow()
                insta_bot._likeTimeLine()
                sleep(3600)

    def _showLinksButton(self, bot, query):
        #این متد برای این است که لینک صفحه اشخاصی که کاربر را آنفالو کرده اند یا بک نداده اند را به او در تلگرام نشان می دهد تا بتواند به صورت دستی در صورتی که نمی تواند از قابلیت آنفالو استفاده کند از این قابلیت مثل اپلیکیشن های اندرویدی استفاده کند
        
        chat_id               = query.message.chat_id
        insta_bot             = self.insta_bot
        driver                = insta_bot.driver
        conn                  = self.connection
        user_database_address = self.user_db_address

        conn.close()
        insta_bot._login()
        insta_bot._updateLinks()
        driver.close()

        unfollowed_links = insta_bot._showLinks(user_database_address)
        len_unflw_links  = unfollowed_links[0]
        unflw_links      = unfollowed_links[1]
        counter          = 1

        for link in unflw_links:
            mathematical_ratio = (counter * 100) / len_unflw_links
            line               = f'{link[0]} - {link[1]} - {mathematical_ratio:.2f}%'

            bot.send_message(chat_id=chat_id, text=line)
            counter += 1
            sleep(1)

        bot.send_message(chat_id=chat_id, text=warning_to_unfollow_persons)






def editActivitiesDatabase(bot_act_db_address, table_name):
    conn = sqlite3.connect(bot_act_db_address)
    cur  = conn.cursor()

    if table_name == "insta_temporary_activities":
        cur.execute(f"DROP TABLE {table_name}")

    elif table_name == "telegram_button":
        cur.execute(f'DELETE FROM {table_name} WHERE button="auto_button" OR button="follow_button"')

    conn.commit()
    conn.close()






def connectApiToSendMessage(token, method, query, message):
    DisconnectionError     = ConnectionError
    NetworkConnectionError = NetworkError
    BadRequests            = BadRequest
    allow                  = True

    while allow:
        try:
            req     = requests.get("https://api.telegram.org/bot" + token + "/getMe")
            code    = req.status_code
            chat_id = query.message.chat_id

            if code == 200:
                url       = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
                _response = requests.post(url=url, data={'chat_id': chat_id, 'text': message})
                allow     = False
        except (DisconnectionError, NetworkConnectionError, BadRequests):
            sleep(30)




def saveError(error, error_file_address):
    error_time = str(datetime.now()).split('.')[0]

    with open(error_file_address, 'a') as file_txt:
        file_txt.write(f"Error is:\n\nfrom  {error.__class__}  :  {str(error)}  -  {error_time}\n\n")
        file_txt.write(f"\t\t\t\t\t======================================================\n\n")





def buttonsHandler(bot, update):
    DisconnectionError = requests.exceptions.ConnectionError
    IntegrityError     = sqlite3.IntegrityError
    query              = update.callback_query
    bot_act_db_name    = str(query.message.chat_id) + "_activities.db"
    bot_act_db_address = activities_db_location + bot_act_db_name

    error_txt_file_name     = str(query.message.chat_id) + "_error_log.txt"
    error_txt_file_location = error_txt_file_address + error_txt_file_name

    insta_temporary_activities_table = "insta_temporary_activities"
    telegram_button_table            = "telegram_button"
    method                           = "sendMessage"


    try:
        connectToBotActivitiesDatabase(bot_act_db_address)

        selected_button = SelectedButtonsHandler(bot, update, users_db_location, bot_act_db_address)
        driver          = selected_button.insta_bot.driver
        conn            = selected_button.connection

        selected_button._buttonChoosed()
    
    #زمانی که مرورگر فایر فاکس در سیستم نصب نباشد این اررو هندل می شود
    except SessionNotCreatedException:
        connectApiToSendMessage(my_bot_token, method, query, error_message_for_browers)
    
    #زمانی که سیستم عامل شخص توسط ربات شناخته نشود و نمونه ای از درایور فایرفاکس وجود نداشته باشد این اررو رخ می دهد
    except AttributeError:
        connectApiToSendMessage(my_bot_token, method, query, error_message_for_oprating_system)

    #زمانی که جدول موقتی ثبت فعالیت ربات به حد نساب خود برسد این اررو هندل می شود که نشان دهند پایان فعالیت موفقیت آمیز ربات است
    except IntegrityError as error:
        driver = selected_button.insta_bot.driver

        saveError(error, error_txt_file_location)
        editActivitiesDatabase(bot_act_db_address, insta_temporary_activities_table)
        driver.close()
        connectApiToSendMessage(my_bot_token, method, query, successfully_message)

    #اررو های دیگر مرتبط با بسته شدن ناگهانی درایور, قطع شدن اینترنت, پیدا نشدن یک المنت در یک صفحه و ارورهای احتمالی دیگر در این قسمت هندل می شوند
    except Exception as error:
        saveError(error, error_txt_file_location)
        editActivitiesDatabase(bot_act_db_address, telegram_button_table)
        conn.close()

        try:
            driver.close()
        except InvalidSessionIdException:
            connectApiToSendMessage(my_bot_token, method, query, close_driver_error_message)
            return

        if isinstance(error, RuntimeError):
            connectApiToSendMessage(my_bot_token, method, query, login_error_message)

        elif isinstance(error, DisconnectionError):
            connectApiToSendMessage(my_bot_token, method, query, connection_error_message)
            
        else:
            connectApiToSendMessage(my_bot_token, method, query, runtime_error_message)



