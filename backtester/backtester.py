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

    def run(self, optimizing: bool):
        """
        Iterate across the rows in the train dataset. This
        set will train the model and check the performance
        of the trading strategy.
        """

        return_optimizer = {
            'train_set': 0,
            'test_set': 0,
            'validation_set': 0
        }

        train_test_info = {}
        returns = {}

        for information_set in ['train', 'test', 'validation']:

            dataset = getattr(self.stock, information_set)

            trade_log = self.iterate_across_set(
                dataset=dataset,
                position_recorder=PositionState(),
            )

            # Convert dicts to dataframes
            equity = pd.DataFrame(trade_log.equity.realised.items(), columns=['time', 'equity']).set_index('time')
            trade_positions = pd.DataFrame(trade_log.tradelog.log).T

            returns[information_set] = equity

            if optimizing:
                return_optimizer[information_set + '_set'] = (equity, trade_positions)

            else:
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

        if optimizing:
            return return_optimizer
        else:
            return train_test_info, returns

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
        long_positions = trade_positions[trade_positions["position_type"] < 'short']["spread"]
        short_positions = trade_positions[trade_positions["position_type"] == 'long']["spread"]

        stats = {
            "equity_start": round(equity["equity"][0], 2),
            "equity_final": round(equity["equity"][-1], 2),
            "equity_peak": round(equity["equity"].max(), 2),
            "return": round(equity["equity"][-1] / equity["equity"][0] * 100, 2),
            "buy_and_hold_return": round(dataset.open[-1] / dataset.open[0] * 100, 2),

            "average_long_position": str(trade_duration[long_positions.index].values.mean()).split('.')[0],
            "average_gain_long_position": round(long_positions[long_positions > 0].mean() * 100, 2),
            "average_loss_long_position": round(long_positions[long_positions < 0].mean() * 100, 2),
            "number_of_long_positions": len(long_positions),
            "win_rate_long_positions": len(long_positions[long_positions > 0]) / len(long_positions),

            "average_short_position": str(trade_duration[short_positions.index].values.mean()).split('.')[0],
            "average_gain_short_position": round(long_positions[long_positions >= 0].mean() * 100, 2),
            "average_loss_short_position": round(long_positions[long_positions <= 0].mean() * 100, 2),
            "number_of_short_positoins": len(short_positions),
            "win_rate_short_positions": len(long_positions[long_positions > 0]) / len(long_positions),

            "number_of_trades": len(trade_positions),
            "win_rate": round(profitable_trades / len(trade_positions), 4),
        }

        return stats
