#!/usr/bin/python3.8


from instagram_bot import my_bot_token
from instagram_bot import InteractWithUser
from instagram_bot import buttonsHandler
from instagram_bot import ConversationHandler, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from instagram_bot import CHOOSING_USERNAME, GETTING_USERNAME, CHOOSING_PASSWORD, GETTING_PASSWORD, START_BUTTON, BUTTON_HANDLER




def conversationWithUser():
    InteractWithUser.wrng._hiddenWarning()
    interact = InteractWithUser(my_bot_token)
    
    convr_handler = ConversationHandler(

        entry_points=
        [
            CommandHandler(interact.cmd.start_cmd, interact.cmd._startCommand)
        ],

        states={
            CHOOSING_USERNAME:
            [
                MessageHandler(Filters.regex('^نام کاربری$'), interact._showEnterUserNameMessage)
            ],

            GETTING_USERNAME: 
            [
                MessageHandler(Filters.command, interact._messageToExecuteCammand),
                MessageHandler(Filters.text, interact._getUserName)
            ],

            CHOOSING_PASSWORD: 
            [
                MessageHandler(Filters.regex('^رمز عبور$'), interact._showEnterPasswordMessage)
            ],

            GETTING_PASSWORD:
            [
                MessageHandler(Filters.command, interact._messageToExecuteCammand),
                MessageHandler(Filters.text, interact._getPassword)
            ],

            START_BUTTON:
            [
                MessageHandler(Filters.regex('^شروع فعالیت$'), interact._clickStartActivity)
            ],

            BUTTON_HANDLER:
            [
                CallbackQueryHandler(buttonsHandler)
            ]

        },

        fallbacks=
        [
            MessageHandler(Filters.regex('^(مرحله قبل|شروع دوباره)$'), interact._backButton),
            CommandHandler(interact.cmd.show_id_cmd, interact.cmd._showIdCommand),
            MessageHandler(Filters.text, interact._waitingMessageForOptions)
        ]
    )

    interact.tel._conversationsHandler(convr_handler)
    interact.tel._keepRunning()



if __name__ == "__main__":
    conversationWithUser()









