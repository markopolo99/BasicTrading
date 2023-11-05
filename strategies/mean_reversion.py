import pandas as pd
from strategies.position_check import PositionCheck

class MeanReversion(PositionCheck):

    def __init__(self, df_prices: pd.DataFrame, window: int):
        self.df_prices = df_prices
        self.window = window
        self.positions = pd.DataFrame(columns=["position"], index=self.df_prices.index)

    def _indicator(self, current_date: pd.Timestamp) -> float:
        """
        Find the mean across the rolling window period
        """
        # Define the start period for the rolling window
        start_date = (current_date.to_period("D") - self.window).to_timestamp()

        # Define the end period to exclude todays date
        end_date = (current_date.to_period("D") - 1).to_timestamp()

        # Extract the prices across which you are finding the mean
        df_prices_window = self.df_prices.loc[start_date:end_date].mean()

        return df_prices_window

    def _position_taking(self, current_date: pd.Timestamp, current_price: float, historical_mean: float) -> None:

        # Check whether we enter or exit positions
        if current_price > historical_mean:
            self.positions.loc[current_date, "position"] = -1
        elif current_price < historical_mean:
            self.positions.loc[current_date, "position"] = 1

        pass