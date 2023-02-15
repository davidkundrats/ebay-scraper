from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd 
import numpy as np
import requests
import tkinter as tk
import customtkinter as ui
import time 
import math
import logging
import ctypes

def run(): 
    linkInput = linkEntry.get() 
    pathInput = pathEntry.get()
    ebayScraper(linkInput, pathInput)

def ebayScraper(input, path): # scrapes user supplied ebay URL link for the first page and returns dataframe with scraped data

     
    itemNames = [] # use to append item names and prices after scrape
    itemPrices = []
    itemDate = []
    
    ebayUrl = input
    path = path
    r = requests.request('GET', ebayUrl, headers ={'User-Agent' : 'Mozilla/5.0'})
    try:
        with requests.Session() as session: # open session 
            soup = BeautifulSoup(r.content,  features= 'html.parser') 
            nameTags = soup.findAll('div', class_ = 's-item__title')
            priceTags = soup.findAll('span', class_ = 's-item__price')
            dateTags = soup.findAll('div', class_ = 's-item__title--tag')

            for date in dateTags: # need to filter out the second span tag identified by class 'clipped' use span tag identified by 'POSITIVE' instead
                extracted = date.find_all('span', class_ = 'POSITIVE')
                for i in range(0, len(extracted)): 
                    itemDate.append(extracted[i].get_text()) #place text in itemDate list

            if(len(nameTags) == len(priceTags)): # need to get rid of bogus first element in both lists
                nameTags.pop(0)
                priceTags.pop(0)

            else: 
                return 'error occured with count of name and price tags: invalid link'  ## if elements aren't even something went wrong in counting the listings
        
            if(len(nameTags) == len(priceTags) == len(itemDate)): # verify lengths are the same otherwise exit with status code
                for i in range(0, len(nameTags)): # all same length doesnt matter which is used for loop 
                    itemNames.append(nameTags[i].get_text())
                    itemPrices.append(priceTags[i].get_text())
                createDf(itemNames, itemPrices, itemDate, path + '/out.csv')
       
            else: 
                return "item count + price count and date count mismatch - unable to tabulate data", -1 #if they arent the same its issue with the date scrape

    except Exception as Argument: 
        logging.exception(Argument)

def createDf(name, price, date, path):  # create dataframe with the data
    path = Path(path)       
    df = pd.DataFrame({'Listed Name': name, 'Sold Price': price, 'Date Sold': date})
    columns = df.columns
    df['Date Sold'] = df['Date Sold'].str.replace('Sold  ?' , '')
    df[columns] = df[columns].replace({'\$':''}, regex= True)
    df.set_index(['Date Sold'], inplace= True)
    path.parent.mkdir(parents = True, exist_ok = True)
    df.to_csv(path)
    print(df)
    displayComplete()

def displayComplete(): 
    popup = ui.CTkToplevel(root)
    popup.geometry("400x150")
    popup.wm_title("Complete!")
    button = ui.CTkButton(master = popup, text = "Visualize Data?", command = visualizeData)
    button.pack(pady = 24, padx = 18)
    
def visualizeData(): 
    pass

ctypes.windll.shcore.SetProcessDpiAwareness(2)

root = ui.CTk()

root.geometry("500x350")


frame = ui.CTkFrame(master = root)
frame.pack(fill = "both", expand = True)

ui.set_appearance_mode("dark") 
ui.set_default_color_theme("dark-blue")

label = ui.CTkLabel(master = frame, text = "Ebay Sold Price Scraper", font=("Roboto", 24))  
label.pack(pady = 12, padx = 10) 


linkEntry = ui.CTkEntry(master = frame, placeholder_text = "Paste ebay link here")
linkEntry.pack(pady = 12, padx = 10)

pathEntry = ui.CTkEntry(master = frame, placeholder_text= "Set path to save csv")
pathEntry.pack(pady = 20, padx = 16)

button = ui.CTkButton(master = frame, text = "Search", command = run)
button.pack(pady = 12, padx = 10)

root.mainloop()



 

