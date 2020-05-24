#!/usr/bin/python3.8

from instagram_bot import Updater, CommandHandler, CallbackQueryHandler
from instagram_bot import basicConfig, INFO



class TelegramBotHandler:

    basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=INFO)

    def __init__(self, token):
        self.token      = token
        self.updater    = Updater(self.token)
        self.dispatcher = self.updater.dispatcher
    
    def _keepRunning(self):
        self.updater.start_polling()
        self.updater.idle()
    
    def _addHandler(self, handler):
        self.dispatcher.add_handler(handler)
    
    def _commandsHandler(self, command, callback_func):
        self._addHandler(CommandHandler(command, callback_func))

    def _callbackQueriesHandler(self, callback_func):
        self._addHandler(CallbackQueryHandler(callback_func))
    
    def _conversationsHandler(self, conv_handler):
        self._addHandler(conv_handler)
    
    def _sendMessage(self, message, bot, update, keyboard_markup=None):
        bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=keyboard_markup)
    
    def _deleteMessage(self, bot, update):
        bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)

    def _replyMessage(self, message, bot, update, keyboard_markup=None):
        update.message.reply_text(message, reply_markup=keyboard_markup)








