import pandas as pd
from backtester.strategy import Strategy


class MACrossover(Strategy):

    def __init__(self, stock_info):
        self.stock_prices

    def long():
        pass

    def short():
        pass

    def close():
        pass

    def _calc_indicator(self):

        self._indicator = pd.DataFrame(index=self.df_prices.index)

        for ma in self.ma_pair:
            self._indicator.loc[:, "ma_" + str(ma)] = self.df_prices.rolling(window=ma).mean()

        self._indicator = self._indicator.fillna(0)

        return self._indicator

    def _position_taking(self, date: pd.Timestamp):

        fast_ma = self._indicator.loc[date, "ma_" + str(self.ma_pair[0])]
        slow_ma = self._indicator.loc[date, "ma_" + str(self.ma_pair[1])]

        if fast_ma > slow_ma:
            _current_condition = True
        else:
            _current_condition = False

        return _current_condition
