#!/usr/bin/python3.8



from instagram_bot import InlineKeyboardButton, InlineKeyboardMarkup


insta_activities_inline_keyboard_buttons = [

    [InlineKeyboardButton('فالو', callback_data='_flw'),
    InlineKeyboardButton('آنفالو', callback_data='_unflw')],

    [InlineKeyboardButton('حالت خودکار', callback_data='_auto')],
    
    [InlineKeyboardButton('لینک پیج کسایی که دیگه شمارو دنبال نمی کنند',callback_data='_links')]
]


insta_activities_inline_keyboard_markup = InlineKeyboardMarkup(insta_activities_inline_keyboard_buttons)






