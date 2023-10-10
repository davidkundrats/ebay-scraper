from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt
import mplcursors
import matplotlib.dates as mdates


def save_csv(df, path):
    """Method to save a DataFrame as a .csv using pathlib library"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)


def avg_price(df):
    """Method used to calculate and visualize the average sold price."""
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
    """Method used to determine if the database connection exists
    if yes: connect, if not, inform user and continue"""
    pass


def add_to_db(df):
    """Method used to add the DataFrame to a database"""
    pass


def retreive_from_db(df):
    """Method used to retreive the DataFrame from the database"""
    pass
