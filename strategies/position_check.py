import pandas as pd
import strategies.constants as cons

class PositionCheck:

    def __init__(self):
        self.df_prices = pd.DataFrame
        self.positions = pd.DataFrame
        self.indicator = pd.DataFrame
        self.current_condition = bool

    def get_positions(self) -> pd.DataFrame:

        # For each point in time, find the indicator value
        self._indicator()
        
        # Store the positions you take in a vector
        self.positions = pd.DataFrame(
            index=self.df_prices.index, 
            columns=["position"]
        )

        for date in self.df_prices.index:
            
            # Update the entry conditoin
            self._position_taking(date)

            # Check whether we long or short the position
            if self.current_condition:
                self.positions.loc[date, "position"] = 1
            elif not self.current_condition: 
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
            self.current_position = "long"
        else:
            self.current_position = "short"

        # Define a variable for the current trade date
        self.current_trade_date = self.positions.index[0]

        # Update the track recrod
        self.trades.loc[self.current_trade_date, "position_type"] = self.current_position
        self.trades.loc[self.current_trade_date, "position_entry"] = self.df_prices[self.current_trade_date]

        # Loop across each day and check when you are in a position
        for date in self.df_prices.index[1:]:
            
            # Check what the current position is
            self._check_position(date=date)

            if self.positions["position"].loc[date] == 1:
                self.current_position = "long"
            else:
                self.current_position = "short"

        pass

    def _check_position(self, date: pd.Timestamp):

        # Check what the market says to do right now and compare it to the currently held position
        if self.current_position == "long" and self.positions["position"].loc[date] == -1:
            self.trades.loc[self.current_trade_date, "position_exit"] = self.df_prices[date]
            
            # After exiting the trade, we enter a new trade in the opposite direction
            self.trades.loc[date, "position_type"] = "short"
            self.trades.loc[date, "position_entry"] = self.df_prices[date]
            self.current_trade_date = date

        elif self.current_position == "short" and self.positions["position"].loc[date] == 1:
            self.trades.loc[self.current_trade_date, "position_exit"] = self.df_prices[date]
            
            # After exiting the trade, we enter a new trade in the opposite direction
            self.trades.loc[date, "position_type"] = "long"
            self.trades.loc[date, "position_entry"] = self.df_prices[date]
            self.current_trade_date = date

        pass

    def _indicator(self):
        pass

    def _position_taking(self):
        pass