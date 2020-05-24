#!/usr/bin/python3.8



from instagram_bot import username_keyboard_markup
from instagram_bot import admin_chat_id, username_button_message, start_command_message, CHOOSING_USERNAME
import time


class CommandsHandler:

    start_cmd    = 'start'
    show_id_cmd  = 'showid'

    def __init__(self, telegram_bot_handler_instance):
        self.tel = telegram_bot_handler_instance

    def _startCommand(self, bot, update):
        self.tel._replyMessage(start_command_message, bot, update, keyboard_markup=username_keyboard_markup)
        time.sleep(30)
        self.tel._replyMessage(username_button_message, bot, update, keyboard_markup=username_keyboard_markup)
        return CHOOSING_USERNAME
    
    def _showIdCommand(self, bot, update):
        message = update.message.chat_id
        self.tel._sendMessage(message, bot, update)









