#!/usr/bin/python3.8



import random


def getValues(address_file, number_of_value=1):
    """value can be hashtag or name so get values from text file"""

    list_values = []
    lst_values  = []

    with open(address_file, 'r') as file_txt:
        while file_txt.readline():
            for value in file_txt.readlines():
                list_values.append(value.strip())
            file_txt.readline()

    while len(lst_values) < number_of_value:
        value = random.choice(list_values)
        if value not in lst_values:
            lst_values.append(value)
    
    return lst_values
