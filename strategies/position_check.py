import pandas as pd
import strategies.constants as cons

class PositionCheck:

    def __init__(self):
        self.df_prices = pd.DataFrame
        self.positions = pd.DataFrame

        self._current_condition = bool
        self._current_position = str
        self._current_trade_date = pd.Timestamp

    def get_positions(self) -> pd.DataFrame:

        # For each point in time, find the indicator value
        self._indicator = self._calc_indicator()
        
        # Store the positions you take in a vector
        self.positions = pd.DataFrame(
            index=self.df_prices.index, 
            columns=["position"]
        )

        for date in self.df_prices.index:
            
            # Update the entry conditoin
            _current_condition = self._position_taking(date)

            # Check whether we long or short the position
            if _current_condition:
                self.positions.loc[date, "position"] = 1
            elif not self._current_condition: 
                self.positions.loc[date, "position"] = -1

        pass
    
    def get_returns(self):
        """
        Translate a boolean vector that represents being long (value of 1)
        or being short (value of -1) into a vector of profitability. 
        """

        # Keep a track record of trades that are entered + some statistics
        self.trades = pd.DataFrame(
            index=self.df_prices.index, 
            columns=cons.TRADING_STATS,
        )

        # Initialize position
        if self.positions["position"].iloc[0] == 1:
            self._current_position = "long"
        else:
            self._current_position = "short"

        # Define a variable for the current trade date
        self._current_trade_date = self.positions.index[0]

        # Update the track recrod
        self.trades.loc[self._current_trade_date, "position_type"] = self._current_position
        self.trades.loc[self._current_trade_date, "position_entry"] = self.df_prices[self._current_trade_date]

        # Loop across each day and check when you are in a position
        for date in self.df_prices.index[1:]:
            
            # Check what the current position is
            self._check_position(date=date)

            if self.positions["position"].loc[date] == 1:
                self._current_position = "long"
            else:
                self._current_position = "short"

        self.trades = self.trades.dropna(how="all")

        pass

    def _check_position(self, date: pd.Timestamp):

        # Check what the market says to do right now and compare it to the currently held position
        if self._current_position == "long" and self.positions["position"].loc[date] == -1:
            self._update_positions(date)

        elif self._current_position == "short" and self.positions["position"].loc[date] == 1:
            self._update_positions(date)

        pass

    def _update_positions(self, date: pd.Timestamp):
        # Short hand notation for current date
        ctd = self._current_trade_date

        # Update other trading statistics
        self.trades.loc[self._current_trade_date, "position_exit"] = self.df_prices[date]
        self.trades.loc[date, "position_entry"] = self.df_prices[date]
        self.trades.loc[date, "hold_duration"] = (date - self._current_trade_date).days

        # After exiting the trade, we enter a new trade in the opposite direction
        if self._current_position == "long":
            self.trades.loc[date, "position_type"] = "short"
            self.trades.loc[ctd, "return"] = self.trades.loc[ctd, "position_exit"] - self.trades.loc[ctd, "position_entry"]
        else:
            self.trades.loc[date, "position_type"] = "long"
            self.trades.loc[ctd, "return"] = self.trades.loc[ctd, "position_entry"] - self.trades.loc[ctd, "position_exit"]

        # Update current trade date
        self._current_trade_date = date

        pass

    def _calc_indicator(self):
        pass

    def _position_taking(self):
        pass