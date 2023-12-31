import pandas as pd
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

        stats = self.get_stats()

        return self.position_train, stats

    def get_stats(self):

        equity = pd.DataFrame(self.position_train.equity.realised)
        unrealised_equity = pd.DataFrame(self.position_train.equity.unrealised)

        # The number of positive trades
        profitable_trades = (self.position_train.tradelog.log["Spread"] > 0).sum()

        # The duration of the trades
        trade_duration = (
            self.position_train.tradelog.log["Exit time"] - self.position_train.tradelog.log.index
        )

        # Indicies with negative and positive trades
        negative_trades = self.position_train.tradelog.log[self.position_train.tradelog.log["Spread"] < 0]["Spread"]

        stats = pd.DataFrame(
            [
                ["equity_start", equity.iloc[0, 1]],
                ["equity_final", equity.iloc[-1, 1]],
                ["equity_peak", unrealised_equity.iloc[:, 1].max()],
                ["return", equity.iloc[-1, 1] / equity.iloc[0, 1]],
                ["buy_and_hold_return", self.stock.train.open[-1] / self.stock.train.open[0]],
                ["volatility", equity.iloc[:, 1].std()],
                ["sharpe_ratio", equity.iloc[:, 1].mean() / equity.iloc[:, 1].std()],
                ["max_drawdown", unrealised_equity.iloc[:, 1].min()],
                ["average_drawdown", negative_trades.mean()],
                ["max_drawdown_duration", str(trade_duration[negative_trades.index].max())],
                ["average_drawdown_duration", str(trade_duration[negative_trades.index].mean())],
                ["number_of_trades", len(self.position_train.tradelog.log)],
                ["win_rate", profitable_trades / len(self.position_train.tradelog.log)],
                ["best_trade", self.position_train.tradelog.log["Spread"].max()],
                ["worst_trade", self.position_train.tradelog.log["Spread"].min()],
                ["average_trade return", self.position_train.tradelog.log["Spread"].mean()],
            ]
        )

        return stats
