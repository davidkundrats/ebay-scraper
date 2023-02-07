import customtkinter as ui, tkinter as tk

ui.set_appearance_mode("dark") 
ui.set_default_color_theme("dark-blue")

root = ui.CTk()

root.geometry("500x350")

frame = ui.CTkFrame(master = root)
frame.pack(pady = 20, padx = 60, fill = "both", expand = True)

label = ui.CTkLabel(master = frame, text = "Ebay Sold Price Scraper", font=("Roboto", 24))  
label.pack(pady = 12, padx = 10) 


entry = ui.CTkEntry(master = frame, placeholder_text = "Paste ebay link here")
entry.pack(pady = 12, padx = 10)

def get_input(): 
    input = entry.get() 
    ebayScraper(input)
    
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd, numpy as np, requests

def ebayScraper(input): # scrapes user supplied ebay URL link for the first page and returns dataframe with scraped data
     
    itemNames = [] # use to append item names and prices after scrape
    itemPrices = []
    itemDate = []
    
    ebayUrl = input
    r = requests.request('GET', ebayUrl, headers ={'User-Agent' : 'Mozilla/5.0'})

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
            return 'error occured with count of name and price tags: revise', -1  ## if elements aren't even something went wrong in counting the listings
        
        if(len(nameTags) == len(priceTags) == len(itemDate)): # verify lengths are the same otherwise exit with status code
            for i in range(0, len(nameTags)): # all same length doesnt matter which is used for loop 
                itemNames.append(nameTags[i].get_text())
                itemPrices.append(priceTags[i].get_text()) 
       
        else: 
            return "item count + price count and date count mismatch - unable to tabulate data", -1 #if they arent the same its issue with the date scrape
    df = pd.DataFrame({'Listed Name': itemNames, 'Prices': itemPrices, 'Dates': itemDate})
    print(df)



button = ui.CTkButton(master = frame, text = "Search", command = get_input)
button.pack(pady = 12, padx = 10)

root.mainloop() 

