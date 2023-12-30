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

    def __init__(self, stock: StockData, strategy: Strategy):
        self.stock = stock
        self.strategy = strategy
        self.position_train = PositionState()
        self.position_test = PositionState()

    def run(self):
        """
        Iterate across the rows in the train dataset. This
        set will train the model and check the performance
        of the trading strategy.
        """

        for date, current_price in self.stock.train.iterrows():

            # Only close if you are in a position, and the close position is true
            if self.position_train.in_position and self.strategy.close(date):
                self.position_train.close_position(
                    current_info=self.stock.train.loc[date],
                )

            # Check conditions for going long and short
            if not self.position_train.in_position and self.strategy.long(date):
                self.position_train.open_position(
                    position_type='long',
                    current_info=self.stock.train.loc[date],
                )
            elif not self.position_train.in_position and self.strategy.short(date):
                self.position_train.open_position(
                    position_type='short',
                    current_info=self.stock.train.loc[date],
                )

            # After each new observation, in case you are in a position
            # calculate the change in equity value - unrealised equity
            if self.position_train.in_position:
                self.position_train.equity.update_unrealised_equity(
                    current_time=date,
                    current_price=self.position_train.entry_price,
                    entry_price=current_price.open,
                    position_size=self.position_train.position_size,
                    position_type=self.position_train.position_type,
                )

        return self.position_train
