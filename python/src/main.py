from pathlib import Path
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
from utils import save_csv, avg_price, determine_db_status, add_to_db, retreive_from_db
import sys
import pandas as pd
import requests
import mplcursors
import matplotlib
import matplotlib.dates as mdates

matplotlib.use("TkAgg")


def run():
    """Activated by default execution. Captures user input and calls
    ebay_scraper method with link_input as an argument"""
    link_input = input("Enter a sold listing URL: ")
    df = ebay_scraper(link_input)
    determine(df)


def ebay_scraper(link_input):
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
                return None
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
            # if elements aren't even something went wrong in counting the listings
            print(name_tags, price_tags)
            raise Exception(
                "error occurred with count of name and price tags: invalid link"
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
                "Unable to tabulate data"
            )  ## TODO: make this more descriptive

    except Exception as argument:
        print >> sys.stderr, argument  ## TODO: make this more descriptive
        return None


def create_df(name, price, date):
    """Creates a DataFrame and truncates '$' and commas present."""
    df = pd.DataFrame({"Listed Name": name, "Sold Price": price, "Date Sold": date})
    columns = df.columns
    df[columns] = df[columns].replace(  # clean out unnecessary strings in rows
        {"\$": "", "\,": "", "\Sold  ?": ""}, regex=True
    )
    # remove sales not related to user search
    df = df[df["Sold Price"].str.contains(pat="to") == False]
    # cast prices as floats as they were scraped as strings
    df["Sold Price"] = df["Sold Price"].astype(float)
    return df


def determine(df):
    """Method to determine which function to call based on user input"""
    if df is None:
        print("Error occurred during data scraping.")
        return
    inputs = input("Enter (S)ave CSV (A)verage price: ")
    if inputs == "A":
        avg_price(df)
    elif inputs == "S":
        path = input("Please enter a path to save data as CSV: ")
        save_csv(df, path)
    else:
        print("Invalid input. Please enter either 'A' or 'S' ")
        determine(df)


if __name__ == "__main__":
    run()
