from pathlib import Path
import logging
from bs4 import BeautifulSoup
import pandas as pd
import requests
import customtkinter as ui
import numpy as np
import mplcursors
import tkinter as tk
from matplotlib import pyplot as plt
from datetime import datetime



global DF


def run():
    """ Activated by search button within GUI. Captures user input 
        from CTkEntry object and calls ebay_scraper method with link input as argument"""
    link_input = input("Enter a sold listing url: ")
    ebay_scraper(link_input)


def ebay_scraper(link_input):
    """Main algorithm of the program. Uses requests library, beautiful soup """
    ebayLink = link_input
    item_names = []  # use to append item names and prices after scrape
    item_prices = []
    item_date = []
    item_links = []

    r = requests.request('GET', ebayLink, headers={
                         'User-Agent': 'Mozilla/5.0'}, timeout=60)
    try:
        soup = BeautifulSoup(r.content,  features='html.parser')
        name_tags = soup.findAll('div', class_='s-item__title')
        price_tags = soup.findAll('span', class_='s-item__price')
        date_tags = soup.findAll('div', class_='s-item__title--tag')
        link_tags = soup.findAll('a', href=True)

        for date in date_tags:  # need to filter out the second span tag
            extracted = date.find_all('span', class_='POSITIVE')
            if (extracted == 'DEFAULT.POSITIVE'):
                return
            for i in range(0, len(extracted)):
                # further clean date string
                item_date.append(extracted[i].get_text())

        for link in link_tags:
            href = link.get('href')  # extract href attribute
            if href:  # ignore if href is empty
                item_links.append(href)
            # need to get rid of bogus first element in both lists

        if len(name_tags) == len(price_tags):
            name_tags.pop(0)
            price_tags.pop(0)
            link_tags.pop(0)


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
            raise Exception('unable to tabulate data') ## TODO: make this more descriptive
            error_label.config
        
        print("Data scrape complete.")
        next_step = input("Enter (S)ave CSV (A)verage price: ")

        determine(next_step)


    except Exception as argument:
        logging.exception(argument) ## TODO: make this more descriptive
        


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
  

def save_csv(path):
    """Method to save df as .csv using pathlib library"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    DF.to_csv(path)


def avg_price():
    """Method used to calculate and visualize the average sold price. """
    DF['Date Sold'] = pd.to_datetime(DF['Date Sold'], format='%b %d %Y')
    ax = plt.gca()
    ax.plot(DF['Date Sold'], DF['Sold Price'], 'o', markersize=4) 
    cursor = mplcursors.cursor(ax, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(DF['Listed Name'][sel.target.index])) 
    plt.show()

def determine(inputs):
   
    if inputs == 'A': 
        avg_price()
    elif input == 'S': 
        path = input("Please enter a path to save data as CSV: ")
        save_csv(path)

run()
