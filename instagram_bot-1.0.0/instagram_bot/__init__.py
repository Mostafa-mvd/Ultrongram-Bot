#!/usr/bin/python3.8



from logging import basicConfig, INFO

from requests.exceptions import ConnectionError

from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler, CallbackQueryHandler, Updater
from telegram.error import NetworkError, BadRequest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException, SessionNotCreatedException


from instagram_bot.back_end.config.config import firefox_driver_address_for_linux32, firefox_driver_address_for_linux64, firefox_driver_address_for_windows32, firefox_driver_address_for_windows64, firefox_driver_address_for_mac
from instagram_bot.back_end.config.config import login_instagram_page, activities_db_location
from instagram_bot.back_end.config.config import hashtags_file_address, names_file_address, users_db_location

from instagram_bot.back_end.general_works import General

from instagram_bot.back_end.database.create_database import connectToUserDatabase, connectToBotActivitiesDatabase

from instagram_bot.back_end.login import loginToAccaunt

from instagram_bot.back_end.detect_user_blocking_from_instagram import CheckBlock

from instagram_bot.back_end.stop_tracking_who_unfollowed_me import StopTracking

from instagram_bot.back_end.update_links import updateLinks

from instagram_bot.back_end.popularity_person import Popularity

from instagram_bot.back_end.login import Login

from instagram_bot.back_end.follow_hashtags import followHashtags

from instagram_bot.back_end.follow_names import followNames

from instagram_bot.back_end.like_followers import LikeTimeLine

from instagram_bot.back_end.file.get_values import getValues

from instagram_bot.back_end.show_links import ShowLinksFromDataBase

from instagram_bot.back_end.main import InstagramBot


from instagram_bot.front_end.config import my_bot_token, get24HourMessage, get7dayMessage, connection_error_message, successfully_message
from instagram_bot.front_end.config import warning_to_click_unfollow_button, error_txt_file_address, runtime_error_message, login_error_message, warning_to_unfollow_persons, close_driver_error_message, error_message_for_oprating_system, error_message_for_browers
from instagram_bot.front_end.config import CHOOSING_USERNAME, GETTING_USERNAME, CHOOSING_PASSWORD, GETTING_PASSWORD, START_BUTTON, BUTTON_HANDLER
from instagram_bot.front_end.config import username_button_message, password_button_message, input_password_message, input_username_message, start_button_message, waiting_message, start_activity_message, choose_option_message, error_message_to_execute_command
from instagram_bot.front_end.config import start_command_message, admin_chat_id



from instagram_bot.front_end.inline_keyboard_buttons import insta_activities_inline_keyboard_markup

from instagram_bot.front_end.keyboard_buttons import username_keyboard_markup, password_keyboard_markup, start_buttons_keyboard_markup, reset_button_keyboard_markup

from instagram_bot.front_end.telegram_bot import TelegramBotHandler

from instagram_bot.front_end.commands import CommandsHandler

from instagram_bot.front_end.bot_warnings import TelegramBotWarningsHandler

from instagram_bot.front_end.get_info import JavaScriptObject

from instagram_bot.front_end.interact_with_users import InteractWithUser

from instagram_bot.front_end.button_selected import buttonsHandler










