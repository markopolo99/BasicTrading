import pandas as pd
from strategies.position_check import PositionCheck

class MACrossover(PositionCheck):

    def __init__(self, df_prices: pd.DataFrame, ma_pair: list):
        super().__init__()
        self.df_prices = df_prices
        self.ma_pair = ma_pair
        self.current_condition = False

    def _indicator(self):
          
        self.indicator = pd.DataFrame(index=self.df_prices.index)

        for ma in self.ma_pair:
            self.indicator.loc[:, "ma_" + str(ma)] = self.df_prices.rolling(window=ma).mean()

        self.indicator = self.indicator.fillna(0)

        pass

    def _position_taking(self, date: pd.Timestamp):
        fast_ma = self.indicator.loc[date, "ma_" + str(self.ma_pair[0])]
        slow_ma = self.indicator.loc[date, "ma_" + str(self.ma_pair[1])]
        
        if fast_ma > slow_ma:
            self.current_condition = True
        else:
            self.current_condition = False

        pass