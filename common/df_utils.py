from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
import mplcursors
import matplotlib
import matplotlib.dates as mdates

matplotlib.use("TkAgg")


def create_df(name, price, date):
    """Creates a DataFrame and truncates '$' and commas present.""""""Creates a DataFrame and cleans up special characters in 'price' column.

    Args:
    - name (list): List of listed names.
    - price (list): List of sold prices.
    - date (list): List of dates.

    Returns:
    - pandas.DataFrame: A DataFrame containing 'Listed Name', 'Sold Price', and 'Date Sold'.
    """
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


def save_csv(df, path):
    """Method to save a DataFrame as a .csv using pathlib library""" """Saves a DataFrame as a .csv file using pathlib.

    Args:
    - df (pandas.DataFrame): DataFrame to be saved.
    - path (str or Path): Path to save the DataFrame as a .csv file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)


def avg_price(df):
    """Calculates and visualizes the average sold price over the last 30 days.

    Args:
    - df (pandas.DataFrame): DataFrame containing 'Date Sold' and 'Sold Price'.

    Returns:
    - None
    """
    df["Date Sold"] = pd.to_datetime(df["Date Sold"], format="%b %d %Y")
    # Filter the DataFrame to keep only the last 30 days
    last_30_days = df["Date Sold"].max() - pd.DateOffset(days=30)
    filtered_df = df[df["Date Sold"] >= last_30_days]

    fig, ax = plt.subplots()
    ax.plot(filtered_df["Date Sold"], filtered_df["Sold Price"], "o", markersize=4)

    median_price = filtered_df["Sold Price"].median()
    ax.axhline(y=median_price, color="r", linestyle="--", label="Median Price")

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    cursor = mplcursors.cursor(ax, hover=True)
    cursor.connect(
        "add",
        lambda sel: sel.annotation.set_text(
            filtered_df["Listed Name"].iloc[sel.target.index]
        ),
    )
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def determine_db_status():
    """Determines the existence of a database connection.

    Returns:
    - None
    """
    pass


def add_to_db(df):
    """Adds a DataFrame to a database.

    Args:
    - df (pandas.DataFrame): DataFrame to be added to the database.

    Returns:
    - None
    """
    pass


def retreive_from_db(df):
   """Retrieves a DataFrame from a database.

    Args:
    - df (pandas.DataFrame): DataFrame to retrieve from the database.

    Returns:
    - None
    """
    pass
