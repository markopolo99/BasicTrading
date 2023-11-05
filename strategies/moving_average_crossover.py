import pandas as pd
 

class MACrossover:

    def __init__(self, df_prices: pd.DataFrame, ma_range: range):
        self.df_prices = df_prices
        self.ma_range = ma_range

    def moving_avg_calc(self):
        
        df_ma = pd.DataFrame(index=self.df_prices.index)

        for ma in self.ma_range:
            df_ma.loc[:, "ma_" + str(ma)] = self.df_prices.rolling(window=ma).mean()


        return df_ma