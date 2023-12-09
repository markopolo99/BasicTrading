import pandas as pd
import yfinance as yf


class Data:

    def __init__(self,
                 prices: pd.Series,
                 indicator: pd.Series,
                 start_date: str,
                 end_date: str,):

        self.prices = prices
        self.indicator = indicator
        self.start_date = start_date
        self.end_date = end_date


class LoadData:
    """
    Granularity possibilities include:
    - 1m, 2m, 5m, 15m
    - 30m, 60m, 90m, 1h
    - 1d, 5d, 1wk, 1mo, 3mo
    """
    def __init__(self,
                 ticker: str,
                 granularity: str,
                 start_date: str,
                 end_date: str,) -> None:

        # Load data from yahoo finance
        self.df_prices = yf.download(ticker, start_date, end_date, interval=granularity)

        # Rename column names to lowercase
        self.df_prices.columns = self.df_prices.columns.str.lower()

        # Remove timezone element from index
        self.df_prices.index = self.df_prices.index.tz_localize(None)


def main():

    # Specify the type of data you want
    ticker = 'DKNG'
    granul = '1h'
    start = '2022-01-01'
    end = '2023-12-01'

    # Load data according to specifications
    df_prices = LoadData(
        ticker=ticker,
        granularity=granul,
        start_date=start,
        end_date=end,).df_prices

    return df_prices


if __name__ == "__main__":
    main()
