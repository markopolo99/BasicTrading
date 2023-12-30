from backtester.data import StockData
from backtester.strategy import Strategy
from backtester.positions import PositionState


class Backtester:
    """
    Loop across the timeseries and check for each new price
    whether the long/short/close conditions are satisfied.

    At each point in time as soon as we close a position, we
    check whether to open a position again in the next time
    point.

    To decide whether a particular strategy is good, we test
    it on both a test and validation set. The test set results
    are shown immediately after the training, and performance
    is measured seperately. We show two measures:
        - Performance in sample
        - Performance out of sample

    """

    def __init__(self, stock: StockData, strat: Strategy):
        self.stock = stock
        self.strategy = strat
        self.position_train = PositionState()
        self.position_test = PositionState()

    def run(self):
        """
        Iterate across the rows in the train dataset. This
        set will train the model and check the performance
        of the trading strategy.
        """

        for date, _ in self.stock.train.iterrows():

            # Only close if you are in a position, and the close position is true
            if self.strategy.close(date) and self.position_train.in_position:
                self.position_train.close_position()

            if self.strategy.long(date) and not self.position_train.in_position:
                self.position_train.open_position(position_type='long')

            elif self.strategy.short(date) and not self.position_train.in_position:
                self.position_train.open_position(position_type='short')

    def get_stats(self):
        pass
