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

    def open_position(self, position_type: str, current_info: pd.Series):
        """
        Once the open condition for long or short is satisfied
        open a position and record the entry price, time, and
        position type.
        """

        # Store the open price, the most recent price
        self.entry_price = current_info["open"]

        # Keep track of the current point in time
        self.entry_time = current_info.index

        # Note down the type of position (long/short)
        self.position_type = position_type
        self.position_size = int(self.equity.available_equity / self.entry_price)

        # Once we enter a position, update the position variable
        self.in_position = True

    def close_position(self, current_info: pd.Series):
        self.exit_price = current_info["close"]
        self.exit_time = current_info.index

        # Pass all the stored information into the tradelog
        self.tradelog.update_log(
            entry_price=self.entry_price,
            exit_price=self.exit_price,
            entry_time=self.entry_time,
            exit_time=self.exit_time,
            position_type=self.position_type,
            position_size=self.position_size,
        )

        # Revert the position variable to false once position is closed
        self.in_position = False


class TradeLog:

    def __init__(self):
        self.log = pd.DataFrame(
            columns=[
                "Entry price",
                "Exit price",
                "Entry time",
                "Exit time",
                "Position type",
                "Position size",
            ],
        )

    def update_log(self,
                   entry_price: float,
                   exit_price: float,
                   entry_time: pd.DatetimeIndex,
                   exit_time: pd.DatetimeIndex,
                   position_type: str,
                   position_size: int,):

        self.log.loc[entry_time] = pd.DataFrame(
            [
                exit_time,
                entry_price,
                exit_price,
                position_type,
                position_size,
            ],
            columns=[
                "Exit time",
                "Entry price",
                "Exit price",
                "Position type",
                "Position size"
            ],
        )


class Equity:

    def __init__(self, equity: int = 10_000):
        self.available_equity = equity
        self.realised = []
        self.unrealised = []

    def unrealised_equity(self,
                          current_time: pd.DatetimeIndex,
                          position_type: str,
                          position_size: int,
                          entry_price: float,
                          current_price: float,):

        if position_type == 'long':
            current_spread = current_price - entry_price
        else:
            current_spread = entry_price - current_price

        self.unrealised.append(
            [
                current_time,
                self.available_equity + current_spread * position_size
            ]
        )

    def realised_equity(self,
                        current_time: pd.DatetimeIndex,
                        position_type: str,
                        position_size: int,
                        entry_price: float,
                        exit_price: float,):

        if position_type == 'long':
            current_spread = exit_price - entry_price
        else:
            current_spread = entry_price - exit_price

        self.realised.append(
            [
                current_time,
                self.available_equity + current_spread * position_size
            ]
        )

        self.available_equity += current_spread * position_size
