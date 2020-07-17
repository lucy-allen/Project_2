#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 17:16:17 2020

@author: lucyallen
"""


import pandas as pd

def convert_to_number_with_null(string):
    price = ''
    #string = str(string)
    if str(string) == 'nan':
        price += '0'
    else:
        for char in string:
            if char.isnumeric():
                price += char
    return int(price)

def distance_conversion(string):
    dist = ''
    if 'beach' in string:
        for char in string:
            if char.isnumeric():
                dist += char
        if dist == '':
            dist = 0
        return int(dist)
    else:
        dist = 'nan'
        return dist

print(distance_conversion('On the beach'))