import pandas as pd
import yfinance as yf


class StockData:
    """
    Store stock information into a retrievable format. In case
    any further information is needed for a trading strategy
    or any adjustments need to be made to the data, do it here.

    We further split the data according to the train, test, and
    validation set. It is split such that 60% of the data is in
    the train set, 20% in the test set, and 20% in the validation
    set.

    You can access:
        - train
        - test
        - validation
        - start_date
        - end_date
    """
    def __init__(self, prices: pd.Series):

        duration = len(prices)

        self.train = prices.iloc[:int(duration * 0.6), :]
        self.test = prices.iloc[int(duration * 0.6):int(duration * 0.8), :]
        self.validation = prices.iloc[int(duration * 0.8):int(duration), :]
        self.start_date = prices.index.min()
        self.end_date = prices.index.max()


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

    stock_obj = StockData(df_prices)

    return stock_obj


if __name__ == "__main__":
    main()
