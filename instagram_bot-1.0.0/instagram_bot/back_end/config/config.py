#!/usr/bin/python3.8

from platform import system
import os

os.chdir(os.path.dirname(__file__))
os.chdir("..")
backend_folder_location = os.getcwd()

oprating_system = system()


if (oprating_system == "Linux") or (oprating_system == "Darwin"):
    users_db_location                = backend_folder_location + '/database/databases/users/'

    activities_db_location           = backend_folder_location + '/database/databases/activities/'

    hashtags_file_address            = backend_folder_location + '/file/txt_files/hashtags'
    
    names_file_address               = backend_folder_location + '/file/txt_files/names'
    
elif (oprating_system == "Windows"):
    users_db_location                = backend_folder_location + '\\database\\databases\\users\\'

    activities_db_location           = backend_folder_location + '\\database\\databases\\activities\\'

    hashtags_file_address            = backend_folder_location + '\\file\\txt_files\\hashtags'

    names_file_address               = backend_folder_location + '\\file\\txt_files\\names'


login_instagram_page                 = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

firefox_driver_address_for_linux32   = '/drivers/geckodriver-v0.26.0-linux32/geckodriver'

firefox_driver_address_for_linux64   = '/drivers/geckodriver-v0.26.0-linux64/geckodriver'

firefox_driver_address_for_mac       = '/drivers/geckodriver-v0.26.0-macos/geckodriver'

firefox_driver_address_for_windows32 = '\\drivers\\geckodriver-v0.26.0-win32\\geckodriver.exe'

firefox_driver_address_for_windows64 = '\\drivers\\geckodriver-v0.26.0-win64\\geckodriver.exe'









