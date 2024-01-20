from backtester.strategy import Strategy


class StrategyDC(Strategy):

    def __init__(self, window_slow, window_fast):
        self.window_fast = window_fast
        self.window_slow = window_slow
        self.ma_position = 'nowhere'

    def strat_data(self, stock_info):
        self.stock_info = stock_info,
        self.fast_ma = stock_info.open.rolling(window=self.window_fast).mean()
        self.slow_ma = stock_info.open.rolling(window=self.window_slow).mean()

    def long(self, date):

        if self.fast_ma[date] > self.slow_ma[date]:
            enter_position = True
            self.ma_position = 'above'
        else:
            enter_position = False

        return enter_position

    def short(self, date):

        if self.fast_ma[date] < self.slow_ma[date]:
            enter_position = True
            self.ma_position = 'below'
        else:
            enter_position = False

        return enter_position

    def close(self, date):
        """
        Check to see if the moving average crosses from above
        or below.
        """
        if self.ma_position == 'below' and self.fast_ma[date] > self.slow_ma[date]:
            close_position = True
        elif self.ma_position == 'above' and self.fast_ma[date] < self.slow_ma[date]:
            close_position = True
        else:
            close_position = False

        return close_position
