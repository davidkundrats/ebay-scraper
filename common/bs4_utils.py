import sys
from bs4 import BeautifulSoup
import requests
from common.df_utils import create_df
import pandas as pd

def ebay_scraper(link_input:str) -> pd.DataFrame :
    """Main algorithm of the program. Uses requests library,
    BeautifulSoup, and returns a DataFrame"""
    ebay_link = link_input
    item_names = []
    item_prices = []
    item_date = []
    item_links = []

    requested = requests.request(
        "GET", ebay_link, headers={"User-Agent": "Mozilla/5.0"}, timeout=60
    )

    try:
        soup = BeautifulSoup(requested.content, features="html.parser")
        name_tags = soup.findAll("div", class_="s-item__title")
        price_tags = soup.findAll("span", class_="s-item__price")
        date_tags = soup.findAll("div", class_="s-item__title--tag")
        link_tags = soup.findAll("a", href=True)

        for date in date_tags:  # need to filter out the second span tag
            extracted = date.find_all("span", class_="POSITIVE")
            if extracted == "DEFAULT.POSITIVE":
                exit(-1) 
            for i in range(0, len(extracted)):
                # further clean date string
                item_date.append(extracted[i].get_text())

        for link in link_tags:
            href = link.get("href")  # extract href attribute
            if href:  # ignore if href is empty
                item_links.append(href)

        # need to get rid of the bogus first element in both lists
        if len(name_tags) == len(price_tags):
            name_tags.pop(0)
            price_tags.pop(0)
            link_tags.pop(0)
        else:
            #if elements aren't even something went wrong in counting the listings
            print(f' Count for listing names: {len(name_tags)}, Count for price tags: {len(price_tags)}') 
            raise Exception(
                "error occurred with count of name and price tags: invalid link. this usually means you are not supplying a sold listings url"
            )

        # verify lengths are the same; otherwise, exit with an exception
        if len(name_tags) == len(price_tags) == len(item_date):
            # all same length doesn't matter which is used for loop
            for i in range(0, len(name_tags)):
                item_names.append(name_tags[i].get_text())
                item_prices.append(price_tags[i].get_text())

            df = create_df(item_names, item_prices, item_date)
            print("Data scrape complete.")
            return df

        else:
            # if they aren't the same, it's an issue with the date scrape
            raise Exception(
                "Unable to tabulate data. incorrect amount of names, dates and prices. further debugging required ", exit(-1)
            )
           
        ## TODO: make this more descriptive

    except Exception as argument:
        print( sys.stderr, argument)  ## TODO: make this more descriptive
        exit(-1)
