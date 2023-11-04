import pandas as pd
 

class MeanReversion:

    def __init__(self, df_prices: pd.DataFrame, window: int):
        self.df_prices = df_prices
        self.window = window
        self.positions = pd.DataFrame(columns=["position"], index=self.df_prices.index)

    def run_simulation(self) -> pd.DataFrame:
        
        # Relevant dates based on window length
        df_relevant = self.df_prices.iloc[self.window:-1].index

        for date in df_relevant:
            
            # For each point in time, find the mean across a window
            mean = self.rolling_window(current_date=date)
            
            # Define the current price
            price = self.df_prices.loc[date]

            # Check whether we long or short the position
            self.position_taking(current_date=date, current_price=price, historical_mean=mean)

        return self.positions

    def rolling_window(self, current_date: pd.Timestamp) -> float:
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

    def position_taking(self, current_date: pd.Timestamp, current_price: float, historical_mean: float) -> None:

        # Check whether we enter or exit positions
        if current_price > historical_mean:
            self.positions.loc[current_date, "position"] = -1
        elif current_price < historical_mean:
            self.positions.loc[current_date, "position"] = 1

        pass