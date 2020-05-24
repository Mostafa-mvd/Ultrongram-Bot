#!/usr/bin/python3.8



from instagram_bot import username_button_message, password_button_message, input_password_message, input_username_message, start_button_message, waiting_message, start_activity_message, choose_option_message, error_message_to_execute_command
from instagram_bot import CHOOSING_USERNAME, GETTING_USERNAME, CHOOSING_PASSWORD, GETTING_PASSWORD, START_BUTTON, BUTTON_HANDLER
from instagram_bot import ReplyKeyboardRemove
from instagram_bot import TelegramBotHandler
from instagram_bot import CommandsHandler
from instagram_bot import TelegramBotWarningsHandler
from instagram_bot import JavaScriptObject
from instagram_bot import insta_activities_inline_keyboard_markup
from instagram_bot import username_keyboard_markup, password_keyboard_markup, start_buttons_keyboard_markup, reset_button_keyboard_markup



class InteractWithUser:

    wrng               = TelegramBotWarningsHandler()
    java_script_object = JavaScriptObject()

    def __init__(self, token):
        self.tel = TelegramBotHandler(token)
        self.cmd = CommandsHandler(self.tel)

    def _showEnterUserNameMessage(self, bot, update):
        self.tel._replyMessage(input_username_message, bot, update, keyboard_markup=ReplyKeyboardRemove())
        return GETTING_USERNAME
    
    def _showEnterPasswordMessage(self, bot, update):
        self.tel._replyMessage(input_password_message, bot, update, keyboard_markup=ReplyKeyboardRemove())
        return GETTING_PASSWORD

    def _getUserName(self, bot, update):
        jso          = self.java_script_object
        text         = update.message.text
        jso.username = text

        self.tel._replyMessage(password_button_message, bot, update, keyboard_markup=password_keyboard_markup)
        return CHOOSING_PASSWORD

    def _getPassword(self, bot, update):
        jso          = self.java_script_object
        text         = update.message.text
        jso.password = text
        
        self.tel._replyMessage(start_button_message, bot, update, keyboard_markup=start_buttons_keyboard_markup)
        return START_BUTTON

    def _backButton(self, bot, update):
        self.tel._replyMessage(username_button_message, bot, update, keyboard_markup=username_keyboard_markup)
        return CHOOSING_USERNAME

    def _waitingMessageForOptions(self, bot, update):
        self.tel._sendMessage(waiting_message, bot, update)
    
    def _messageToExecuteCammand(self, bot, update):
        self.tel._sendMessage(error_message_to_execute_command, bot, update)

    def _clickStartActivity(self, bot, update):
        self.tel._replyMessage(choose_option_message, bot, update, keyboard_markup=insta_activities_inline_keyboard_markup)

        self.tel._sendMessage(start_activity_message, bot, update, keyboard_markup=reset_button_keyboard_markup)
        return BUTTON_HANDLER




