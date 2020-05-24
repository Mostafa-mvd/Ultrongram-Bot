#!/usr/bin/python3.8

import sys, warnings


class TelegramBotWarningsHandler:
    
    def __init__(self):
        pass

    def _hiddenWarning(self):
        if not(sys.warnoptions):
            warnings.simplefilter("ignore")






