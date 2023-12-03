import pandas as pd


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
