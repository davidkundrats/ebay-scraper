from pathlib import Path
import ctypes
import logging
from bs4 import BeautifulSoup
import pandas as pd
import requests
import customtkinter as ui
import numpy as np
from matplotlib import pyplot as plt

global DF


def run():
    """ Activated by search button within GUI. Captures user input 
        from CTkEntry object and calls ebay_scraper method with link input as argument"""
    link_input = link_entry.get()
    ebay_scraper(link_input)


def ebay_scraper(input):
    """Main algorithm of the program. Uses requests library, beautiful soup """
    ebayLink = input
    item_names = []  # use to append item names and prices after scrape
    item_prices = []
    item_date = []

    r = requests.request('GET', ebayLink, headers={'User-Agent': 'Mozilla/5.0'}, timeout = 60)
    try:
        soup = BeautifulSoup(r.content,  features='html.parser')
        name_tags = soup.findAll('div', class_='s-item__title')
        price_tags = soup.findAll('span', class_='s-item__price')
        date_tags = soup.findAll('div', class_='s-item__title--tag')

        for date in date_tags:  # need to filter out the second span tag
            extracted = date.find_all('span', class_='POSITIVE')
            for i in range(0, len(extracted)):
                # place text in itemDate list
                item_date.append(extracted[i].get_text())

            # need to get rid of bogus first element in both lists
        if len(name_tags) == len(price_tags):
            name_tags.pop(0)
            price_tags.pop(0)

        else:
            # if elements aren't even something went wrong in counting the listings
            print(name_tags, price_tags)
            raise Exception('error occured with count of name and price tags: invalid link')

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


def create_df(name, price, date):
    """Creates dataframe and cleans data of '$' and commas present. Calls display 
    complete method after df is succesfully generated."""
    global DF
    DF = pd.DataFrame(
        {'Listed Name': name, 'Sold Price': price, 'Date Sold': date})

    DF['Date Sold'] = DF['Date Sold'].str.replace('Sold  ?', '')  # clean data
    columns = DF.columns
    DF[columns] = DF[columns].replace({'\$': ''}, regex=True)
    # cast prices as ints as they were scraped as strings
    DF['Sold Price'] = DF['Sold Price'].astype(float)
    DF.set_index(['Date Sold'], inplace=True)

    display_complete()  # route to next page


def display_complete():
    """Create popup window with several methods of visualizing scraped 
    data. Allows user to save dataframe as a .csv to a specified location on the drive."""
    popup = ui.CTkToplevel(root)
    popup.geometry("500x450")
    popup.wm_title("Complete!")
    label = ui.CTkLabel(
        master=popup, text="Generated Dataframe. Plot options below or save as CSV")
    label.pack(pady=12, padx=9)
    path_entry = ui.CTkEntry(
        master=popup, placeholder_text="Set path to save csv")
    path_entry.pack(pady=20, padx=16)
    plot_button = ui.CTkButton(
        master=popup, text="Average Price", command=avg_price)
    plot_button.pack(pady=24, padx=18)
    save_to_csvbutton = ui.CTkButton(
        master=popup, text="Save", command=save_csv)
    save_to_csvbutton.pack(pady=32, padx=24)


def save_csv():
    """Method to save df as .csv using pathlib library"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    DF.to_csv(path)


def avg_price():
    """Method used to calculate and visualize the average sold price. Connected via a CTk button 
    in the popup window. """
    plt.plot()
    plt.show()


ctypes.windll.shcore.SetProcessDpiAwareness(2)

root = ui.CTk()

root.geometry("500x175")


frame = ui.CTkFrame(master=root)
frame.pack(fill="both", expand=True)

ui.set_appearance_mode("dark")
ui.set_default_color_theme("dark-blue")

label = ui.CTkLabel(
    master=frame, text="Ebay Sold Price Scraper", font=("Roboto", 24))
label.pack(pady=12, padx=10)


link_entry = ui.CTkEntry(master=frame, placeholder_text="Paste ebay link here")
link_entry.pack(pady=12, padx=10)

button = ui.CTkButton(master=frame, text="Search", command=run)
button.pack(pady=12, padx=10)

root.mainloop()
