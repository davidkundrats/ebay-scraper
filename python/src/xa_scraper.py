from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd, numpy as np, requests

def xaScraper(): # scrapes predetermined ebay URL link for the first 5 pages and returns dataframe with scraped data
    itemNames = [] # use to append item names and prices after scrape
    itemPrices = []
    itemDate = []

    ebayUrl = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=olympus+xa&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"  # figure out how to optimize this to be speciifc to one certain item without hardcoding it (maybe use key listeners??)
    r = requests.request('GET', ebayUrl, headers ={'User-Agent' : 'Mozilla/5.0'})

    with requests.Session() as session: # open session 
        soup = BeautifulSoup(r.content,  features= 'html.parser') 
        nameTags = soup.findAll('div', class_ = 's-item__title')
        priceTags = soup.findAll('span', class_ = 's-item__price')
        dateTags = soup.findAll('div', class_ = 's-item__title--tag')

        for date in dateTags: # need to filter out the second span tag identified by class 'clipped' 
            extracted = date.find_all('span', class_ = 'POSITIVE')
            for i in range(0, len(extracted)): 
                itemDate.append(extracted[i].get_text()) #place text in itemDate list
                # genreric update
        if(len(nameTags) == len(priceTags)): # need to get rid of bogus first element in both lists
            nameTags.pop(0)
            priceTags.pop(0)

        else: 
            return 'error occured with count of name and price tags: revise', -1  ## if elements aren't even something went wrong in counting the listings
        
        if(len(nameTags) == len(priceTags) == len(itemDate)): # verify lengths are the same otherwise exit with status code
            for i in range(0, len(nameTags)): # all same length doesnt matter length of loop
                itemNames.append(nameTags[i].get_text())
                itemPrices.append(priceTags[i].get_text()) 
       
        else: 
            return "item count + price count and date count mismatch - unable to tabulate data", -1 #if they arent the same its issue with the date scrape
    df = pd.DataFrame({'Listed Name': itemNames, 'Prices': itemPrices, 'Dates': itemDate})
    print(df)
xaScraper()
