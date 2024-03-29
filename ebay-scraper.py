
from common.df_utils import (
    save_csv,
    avg_price,
    determine_db_status,
)
from common.bs4_utils import ebay_scraper
import pandas as pd

def run():
    """Activated by default execution. Captures user input and calls
    ebay_scraper method with link_input as an argument"""
    link_input = input(
        "For best results, scroll down and select 'Show 240 items' on ebay's website.\nEnter a sold listing URL: "
    )
    df = ebay_scraper(link_input)
    determine(df)

    if df is None:
        print("Error occurred during data scraping.")
        return
    inputs = input(
        "Enter input: \n (S)ave CSV \n (A)verage price \n (Q)uit \n (C)onnect to Database \n"
    )
    match inputs:
        case "S":
            postfix = ".csv"
            path = input("Enter path to save CSV file locally: \n")
            path+=(postfix)
            save_csv(df, path) 
            determine(df) 
        case "A":
            avg_price(df)
        case "Q":
            print("Exiting...")
            return
        case "D":
            determine_db_status()
            determine(df)
        case _:
            print("Invalid input. Please try again.")
            determine(df)


if __name__ == "__main__":
    run()
