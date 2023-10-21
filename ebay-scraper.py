from common.df_utils import (
    save_csv,
    avg_price,
    determine_db_status,
)
from common.bs4_utils import ebay_scraper


def run():
    """Activated by default execution. Captures user input and calls
    ebay_scraper method with link_input as an argument"""
    link_input = input(
        "For best results, scroll down and select 'Show 240 items' on ebay's website.\nEnter a sold listing URL: "
    )
    df = ebay_scraper(link_input)
    determine(df)


def determine(df):
    """Method to determine which function to call based on user input"""
    if df is None:
        print("Error occurred during data scraping.")
        return
    inputs = input(
        "Enter input: \n (S)ave CSV \n (A)verage price \n (Q)uit \n (C)onnect to Database \n"
    )
    match inputs:
        case "S":
            save_csv(df)
        case "A":
            avg_price(df)
        case "Q":
            print("Exiting...")
            return
        case "D":
            determine_db_status(df)
        case _:
            print("Invalid input. Please try again.")
            determine(df)


if __name__ == "__main__":
    run()
