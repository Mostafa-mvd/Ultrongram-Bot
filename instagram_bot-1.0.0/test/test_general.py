#!/usr/bin/python3.8


import unittest
from instagram_bot import firefox_driver_address_for_linux64, General
import os
import warnings
from selenium import webdriver
from unittest.mock import patch
from requests.exceptions import ConnectionError



class TestGeneral(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        os.chdir(".")
        gecko_path = os.getcwd() + "/back_end" + firefox_driver_address_for_linux64
        print(gecko_path)

        cls.driver = webdriver.Firefox(executable_path=gecko_path)
        cls.general = General(cls.driver)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
    
    def test_sendRequestsForCheckConnection(self):
        # with self.assertRaises(ConnectionError):
        #     _code = self.general._sendRequestsForCheckConnection("https://instagram.com")


        with patch("instagram_bot.back_end.general_works.requests.get") as mocked_get:
            mocked_get.return_value.status_code = 503
            _code = self.general._sendRequestsForCheckConnection("https://instagram.com")
            self.assertEqual(_code, 503)
            mocked_get.assert_called_with("https://instagram.com")


            mocked_get.return_value.status_code = 200
            _code = self.general._sendRequestsForCheckConnection("https://instagram.com")
            self.assertEqual(_code, 200)
            mocked_get.assert_called_with("https://instagram.com")
    
    def test_randomTimeToSleep(self):
        with self.assertRaises(IndexError):
            self.general._randomTimeToSleep(20, 10)
            self.general._randomTimeToSleep(30, 20)

        self.general._randomTimeToSleep(5, 10)
        self.general._randomTimeToSleep(10, 30)
    
    def test_openPage(self):
        with patch("instagram_bot.back_end.general_works.requests.get") as mocked_get:
            with self.assertRaises(RuntimeError):
                mocked_get.return_value.status_code = 503
                self.general._openPage("https://google.com")
                mocked_get.assert_called_with("https://google.com")
            
            mocked_get.return_value.status_code = 200
            self.general._openPage("https://google.com")
            mocked_get.assert_called_with("https://google.com")
            



if __name__ == "__main__":
    unittest.main()
