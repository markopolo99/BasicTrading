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

        # Close any position that remains open after the end of the period
        if self.position_train.in_position and self.strategy.close(date):
            self.position_train.close_position(
                current_info=self.stock.train.loc[date],
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
                ["equity_start", round(equity.iloc[0, 1], 2)],
                ["equity_final", round(equity.iloc[-1, 1], 2)],
                ["equity_peak", round(unrealised_equity.iloc[:, 1].max(), 2)],
                ["return", round(equity.iloc[-1, 1] / equity.iloc[0, 1], 4)],
                ["buy_and_hold_return", round(self.stock.train.open[-1] / self.stock.train.open[0], 4)],
                ["volatility", round(equity.iloc[:, 1].std(), 4)],
                ["sharpe_ratio", round(equity.iloc[:, 1].mean() / equity.iloc[:, 1].std(), 4)],
                ["max_drawdown", round(unrealised_equity.iloc[:, 1].min(), 2)],
                ["average_drawdown", round(negative_trades.mean(), 4)],
                ["max_drawdown_duration", str(trade_duration[negative_trades.index].max())],
                ["average_drawdown_duration", str(trade_duration[negative_trades.index].mean()).split('.')[0]],
                ["number_of_trades", len(self.position_train.tradelog.log)],
                ["win_rate", round(profitable_trades / len(self.position_train.tradelog.log), 4)],
                ["best_trade", round(self.position_train.tradelog.log["Spread"].max(), 3)],
                ["worst_trade", round(self.position_train.tradelog.log["Spread"].min(), 3)],
                ["average_trade return", round(self.position_train.tradelog.log["Spread"].mean(), 3)],
            ]
        )

        return stats
