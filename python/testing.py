from pathlib import Path
import ctypes
import logging
from bs4 import BeautifulSoup
import pandas as pd
import requests
import customtkinter as ui
import numpy as np
from matplotlib import pyplot as plt
import re

"""Testing enviornment for functions"""


def run():
    """ Activated by search button within GUI. Captures user input 
        from CTkEntry object and calls ebay_scraper method with link input as argument"""
    print('paste ebay link')
    sc = input()

    ebay_scraper(sc)


def ebay_scraper(input):
    """Main algorithm of the program. Uses requests library, beautiful soup """
    ebayLink = input
    item_names = []  # use to append item names and prices after scrape
    item_prices = []
    item_date = []

    r = requests.request('GET', ebayLink, headers={
                         'User-Agent': 'Mozilla/5.0'}, timeout=60)
    try:
        soup = BeautifulSoup(r.content,  features='html.parser')
        name_tags = soup.findAll('div', class_='s-item__title')
        price_tags = soup.findAll('span', class_='s-item__price')
        date_tags = soup.findAll('div', class_='s-item__title--tag')

        for date in date_tags:  # need to filter out the second span tag
            extracted = date.find_all('span', class_='POSITIVE')
            if (extracted == 'DEFAULT.POSITIVE'):
                return
            for i in range(0, len(extracted)):
                # further clean date string
                item_date.append(extracted[i].get_text())

            # need to get rid of bogus first element in both lists
        if len(name_tags) == len(price_tags):
            name_tags.pop(0)
            price_tags.pop(0)

        else:
            # if elements aren't even something went wrong in counting the listings
            print(name_tags, price_tags)
            raise Exception(
                'error occured with count of name and price tags: invalid link')

        # verify lengths are the same otherwise exit with status code
        if len(name_tags) == len(price_tags) == len(item_date):
            # all same length doesnt matter which is used for loop
            for i in range(0, len(name_tags)):
                item_names.append(name_tags[i].get_text())
                item_prices.append(price_tags[i].get_text())
            create_df(item_names, item_prices, item_date)

        else:
            # if they arent the same its issue with the date scrape
            raise Exception('unable to tabulate data')

    except Exception as argument:
        logging.exception(argument)


def date_maker(string):
    match string:
        case 'Jan':
            return "01"
        case 'Feb':
            return '02'
        case 'Mar':
            return '03'
        case 'Apr':
            return '04'
        case 'May':
            return '05'
        case 'Jun':
            return '06'
        case 'Jul':
            return '07'
        case 'Aug':
            return '08'
        case 'Sep':
            return '09'
        case 'Oct':
            return '10'
        case 'Nov':
            return '11'
        case 'Dec':
            return '12'


def create_df(name, price, date):
    """Creates dataframe and cleans data of '$' and commas present. Calls display 
    complete method after df is succesfully generated."""
    global DF
    DF = pd.DataFrame(
        {'Listed Name': name, 'Sold Price': price, 'Date Sold': date})

    columns = DF.columns
    DF[columns] = DF[columns].replace(  # clean out uneccesary strings in rows
        {'\$': '', '\,': '', '\Sold  ?': ''}, regex=True)

    # remove sales not related to user search
    DF = DF[DF['Sold Price'].str.contains(pat='to') == False]

    # cast prices as ints as they were scraped as strings
    DF['Sold Price'] = DF['Sold Price'].astype(float)


def price_filter(entry):
    """Filter sales prices based on user given int"""
    print("filter based on price")
    filter = float(entry)
    global DF
    DF = DF[DF['Sold Price'] >= filter]
    print(DF)


run()
