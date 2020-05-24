#!/usr/bin/python3.8



from instagram_bot import InlineKeyboardButton, InlineKeyboardMarkup


insta_activities_inline_keyboard_buttons = [

    [InlineKeyboardButton('فالو - follow', callback_data='_flw'),
    InlineKeyboardButton('آنفالو - unfollow', callback_data='_unflw')],

    [InlineKeyboardButton('حالت خودکار - auto mode', callback_data='_auto')],
    
    [InlineKeyboardButton('کسایی که شمارو دنبال نمی کنند - who unfollowed you',callback_data='_links')]
]


insta_activities_inline_keyboard_markup = InlineKeyboardMarkup(insta_activities_inline_keyboard_buttons)






