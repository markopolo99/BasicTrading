import pandas as pd


class PositionState:
    """
    Keep track of positions that are taken. In case you
    enter a position, record it in the tradelog once the
    position is closed.
    """

    def __init__(self, equity: int = 10_000):
        self.in_position = False
        self.tradelog = TradeLog()
        self.equity = Equity(equity)
        self.trade_number = 0

    def open_position(self, position_type: str, current_info: dict):
        """
        Once the open condition for long or short is satisfied
        open a position and record the entry price, time, and
        position type.
        """

        # Note down the type of position (long/short)
        position_size = int(self.equity.available_equity / current_info.open)

        self.tradelog.update_entry(
            entry_price=current_info.open,
            entry_time=current_info.Index,
            position_type=position_type,
            position_size=position_size,
        )

        # Once we enter a position, update the position variable
        self.in_position = True

    def close_position(self, current_info: pd.Series):

        # Update equity available after position is closed
        spread = self.equity.update_realised_equity(
            tradelog=self.tradelog.log['trade_' + str(self.trade_number)],
            current_time=current_info.Index,
            exit_price=current_info.open,
        )

        self.trade_number += 1

        # Pass all the stored information into the tradelog
        self.tradelog.update_exit(
            exit_price=current_info.open,
            exit_time=current_info.Index,
            spread=spread,
        )

        # Revert the position variable to false once position is closed
        self.in_position = False


class TradeLog:

    def __init__(self):
        self.log = {}
        self.trade_number = 0

    def update_entry(self,
                     entry_price: float,
                     entry_time: pd.DatetimeIndex,
                     position_type: str,
                     position_size: int,):

        self.log['trade_' + str(self.trade_number)] = {
            'entry_price': entry_price,
            'entry_time': entry_time,
            'position_type': position_type,
            'position_size': position_size,
        }

    def update_exit(self,
                    exit_price: float,
                    exit_time: pd.DatetimeIndex,
                    spread: float,):

        self.log['trade_' + str(self.trade_number)].update(
            {
                'exit_price': exit_price,
                'exit_time': exit_time,
                'spread': spread,
            }
        )

        self.trade_number += 1


class Equity:

    def __init__(self, equity: int = 10_000):
        self.available_equity = equity
        self.realised = {}
        self.unrealised = {}

    def update_realised_equity(self,
                               tradelog: TradeLog,
                               current_time: pd.DatetimeIndex,
                               exit_price: float,):

        if tradelog['position_type'] == 'long':
            spread = exit_price - tradelog['entry_price']
        else:
            spread = tradelog['entry_price'] - exit_price

        self.realised[current_time] = self.available_equity + spread * tradelog['position_size']

        self.available_equity += spread * tradelog['position_size']

        return spread
