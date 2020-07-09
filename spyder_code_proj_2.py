#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:49:35 2020

@author: lucyallen
"""


from bs4 import BeautifulSoup
import requests
import time, os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

import pandas as pd

def get_website(num):
    #query = "stone-harbor-nj-usa/page:{}/filter:95" #have this as an input
    vrbo_search = "https://www.vrbo.com/search/keywords:stone-harbor-nj-usa/page:{number}/filter:95".format(number=num)
    #vrbo_query = vrbo_search + query.replace(' ', '-')

    driver = webdriver.Chrome(chromedriver)
    driver.get(vrbo_search)
    time.sleep(3)
    for i in range(55):
        #Scroll
        driver.execute_script("window.scrollBy(0, 250);")
        #Wait for page to load
        time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    full_page = soup.find('div', class_='HitCollection')
    return full_page
    

def get_price(page):
    prices = []
    for amount in page.find_all('div', class_='HitInfo__price'):
        prices += [amount.text.strip()]
    return prices

def get_distance(page):
    distances = []
    for words in page.find_all('span', class_='GeoDistance__text'):
        distances += [words.text.strip()]
    return distances
    
def get_details(page):
    single_house = page.find_all('div', class_='media-flex__body')
    details = [item.find_all('div', class_ = 'HitInfo__details') for item in single_house]
    index = [str(i) for i in range(50)]
    detail_dict = {}
    for value in index:
        detail_dict[value] = []
    iteration = 0
    for item in details:
        for thing in item:
            for piece in thing.find_all('div'):
                detail_dict[str(iteration)] += [piece.text.strip()]
        iteration += 1
    return detail_dict

def get_ratings(page):
    ratings = []
    for value in page.find_all('span', class_='Rating__ratingcount'):
        ratings += [value.text.strip()]
    return ratings

def make_table(detail_dict, prices, distances, ratings):
    types = []
    for i in range(50):
        types += [detail_dict[str(i)][0]]
    beds = []
    for i in range(50):
        beds += [detail_dict[str(i)][1]]
    baths = []
    for i in range(50):
        baths += [detail_dict[str(i)][2]]
    halfbaths = []
    for i in range(50):
        if 'HF' in detail_dict[str(i)][3]:
            halfbaths += [detail_dict[str(i)][3]]
        else:
            halfbaths += [None]
    sleeps = []
    for i in range(50):
        if 'Sleeps' in detail_dict[str(i)][3]:
            sleeps += [detail_dict[str(i)][3]]
        elif 'Sleeps' in detail_dict[str(i)][4]:
            sleeps += [detail_dict[str(i)][4]]
        else:
            sleeps += [None]
    headers = ['prices','type', 'beds', 'baths', 'halfs', 'sleeps', 'distances', 'ratings']
    rental_lists = [prices, types, beds, baths, halfbaths, sleeps, distances, ratings]
    rental_data = pd.DataFrame(rental_lists)
    return rental_data

def create_tables(num_pages):
    for i in range(1,num_pages+1):
        full_page = get_website(int(i))
        time.sleep(3)
        detail_dict = get_details(full_page)
        prices = get_price(full_page)
        distances = get_distance(full_page)
        ratings = get_ratings(full_page)
        table = make_table(detail_dict,prices,distances,ratings)
        table.to_csv('Table_{page_num}'.format(page_num=i))
        #print(detail_dict)
        #print(distances)
        #print(prices)
        #print(ratings)
create_tables(6)

        
'''
prices = []
for amount in full_page.find_all('div', class_='HitInfo__price'):
    prices += [amount.text.strip()]
distances = []
for words in full_page.find_all('span', class_='GeoDistance__text'):
    distances += [words.text.strip()]
'''