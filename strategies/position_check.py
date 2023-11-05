import pandas as pd


class PositionCheck:

    def __init__(self):
        self.df_prices = pd.DataFrame
        self.positions = pd.DataFrame
        self.indicator = pd.DataFrame
        self.current_condition = bool

    def run_simulation(self) -> pd.DataFrame:

        # For each point in time, find the indicator value
        self._indicator()
        
        # Store the positions you take in a vector
        self.positions = pd.DataFrame(index=self.df_prices.index, columns=["position"])

        for date in self.df_prices.index:
            
            # Update the entry conditoin
            self._position_taking(date)

            # Check whether we long or short the position
            if self.current_condition:
                self.positions.loc[date, "position"] = 1
            elif not self.current_condition: 
                self.positions.loc[date, "position"] = -1

        pass
    
    def _indicator(self):
        pass

    def _position_taking(self):
        pass