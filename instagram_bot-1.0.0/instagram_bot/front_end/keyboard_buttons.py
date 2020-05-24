#!/usr/bin/python3.8


from instagram_bot import ReplyKeyboardMarkup



username_keyboard_button = [['نام کاربری']]

password_keyboard_buttons = [['رمز عبور', 'مرحله قبل']]

start_keyboard_buttons = [['شروع فعالیت', 'مرحله قبل']]

reset_keyboard_button = [['شروع دوباره']] 


username_keyboard_markup = ReplyKeyboardMarkup(username_keyboard_button, one_time_keyboard=True, resize_keyboard=True)

password_keyboard_markup = ReplyKeyboardMarkup(password_keyboard_buttons, one_time_keyboard=True, resize_keyboard=True)

start_buttons_keyboard_markup = ReplyKeyboardMarkup(start_keyboard_buttons, one_time_keyboard=True, resize_keyboard=True)

reset_button_keyboard_markup = ReplyKeyboardMarkup(reset_keyboard_button, one_time_keyboard=True, resize_keyboard=True)











