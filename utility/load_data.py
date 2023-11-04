import pandas as pd
import yfinance as yf
from datetime import datetime

def load_data(start_date: str, ticker: str, granularity: str) -> pd.DataFrame:

    # Set end_date to be today
    end_date = str(datetime.now().date())

    # Load data from yahoo finance
    df_raw = yf.download(ticker, start_date, end_date, interval=granularity)

    # Rename column names to lowercase
    df_raw.columns = df_raw.columns.str.lower()
    
    # Remove timezone element from index
    df_raw.index = df_raw.index.tz_localize(None)

    return df_raw
