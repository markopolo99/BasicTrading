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

    def run(self):
        """
        Iterate across the rows in the train dataset. This
        set will train the model and check the performance
        of the trading strategy.
        """

        train_test_info = {}

        for information_set in ['train', 'test', 'validation']:

            dataset = getattr(self.stock, information_set)

            trade_log = self.iterate_across_set(
                dataset=dataset,
                position_recorder=PositionState(),
            )

            # Convert dicts to dataframes
            equity = pd.DataFrame(trade_log.equity.realised.items(), columns=['time', 'equity']).set_index('time')
            trade_positions = pd.DataFrame(trade_log.tradelog.log).T

            stats = self.get_stats(
                equity=equity,
                trade_positions=trade_positions,
                dataset=dataset,
            )

            train_test_info[information_set] = {
                'equity_' + information_set: equity,
                'trade_positions_' + information_set: trade_positions,
                'stats_' + information_set: stats,
            }

        return train_test_info

    def iterate_across_set(self, position_recorder: PositionState, dataset: StockData):

        self.strategy.strat_data(dataset)

        for row in dataset.itertuples():

            # Only close if you are in a position, and the close position is true
            if position_recorder.in_position and self.strategy.close(row.Index):
                position_recorder.close_position(
                    current_info=row,
                )

            # Check conditions for going long and short
            if not position_recorder.in_position and self.strategy.long(row.Index):
                position_recorder.open_position(
                    position_type='long',
                    current_info=row,
                )
            elif not position_recorder.in_position and self.strategy.short(row.Index):
                position_recorder.open_position(
                    position_type='short',
                    current_info=row,
                )

        # Close any position that remains open after the end of the period
        if position_recorder.in_position:
            position_recorder.close_position(
                current_info=row,
            )

        return position_recorder

    def get_stats(self, equity, trade_positions, dataset):

        # The number of positive trades
        profitable_trades = (trade_positions["spread"] > 0).sum()

        # The duration of the trades
        trade_duration = (
            trade_positions["exit_time"] - trade_positions["entry_time"]
        )

        # Indicies with negative and positive trades
        negative_trades = trade_positions[trade_positions["spread"] < 0]["spread"]
        positive_trades = trade_positions[trade_positions["spread"] >= 0]["spread"]

        stats = {
            "equity_start": round(equity["equity"][0], 2),
            "equity_final": round(equity["equity"][-1], 2),
            "equity_peak": round(equity["equity"].max(), 2),
            "return": round(equity["equity"][-1] / equity["equity"][0] * 100, 2),
            "buy_and_hold_return": round(dataset.open[-1] / dataset.open[0] * 100, 2) ,
            "volatility": round(equity["equity"].std(), 4),
            "sharpe_ratio": round(equity["equity"].mean() / equity["equity"].std(), 4),
            "max_drawdown": round(equity["equity"].min(), 2),
            "average_drawdown": round(negative_trades.mean(), 4),
            "max_drawdown_duration": str(trade_duration[negative_trades.index].max()),
            "average_drawdown_duration": str(trade_duration[negative_trades.index].mean()).split('.')[0],
            "average_upward_duration": str(trade_duration[positive_trades.index].mean()).split('.')[0],
            "average_trade_duration": str(trade_duration.mean()).split('.')[0],
            "number_of_trades": len(trade_positions),
            "win_rate": round(profitable_trades / len(trade_positions), 4),
            "best_trade": round(trade_positions["spread"].max(), 3),
            "worst_trade": round(trade_positions["spread"].min(), 3),
            "average_trade return": round(trade_positions["spread"].mean(), 3),
        }

        return stats
