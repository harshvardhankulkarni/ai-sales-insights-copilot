"""Load the daily sales DataFrame.

The only job of this module: turn data/sales.csv into a DataFrame.
Nothing else lives here.
"""

import pandas as pd

DATA_FILE = "data/sales.csv"


def load_sales(path: str = DATA_FILE) -> pd.DataFrame:
    """Read the CSV and return a DataFrame with columns:
    date (datetime), revenue (float), units (int).
    """
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def last_days(df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    """Return only the most recent `days` rows of the DataFrame."""
    return df.tail(days)