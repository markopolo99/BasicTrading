import pandas as pd

from backtester.data import LoadData, StockData
from backtester.backtester import Backtester
from backtester.plotter import Plotter

from strategies.strategy_crossover import StrategyDC
import sys
sys.path.append("C:\\Users\\tomic\\Desktop\\BasicStrategy\\BasicTrading")

# Specify the type of data you want
ticker = 'DKNG'
granul = '1h'
start = '2022-03-01'
end = '2023-12-01'

# Load data according to specifications
df_prices = LoadData(
    ticker=ticker,
    granularity=granul,
    start_date=start,
    end_date=end,).df_prices

stock_obj = StockData(df_prices)
strategy_obj = StrategyDC(
    stock_obj,
    window_fast=5,
    window_slow=10,
)

backtest_results, stats = Backtester(
    stock=stock_obj,
    strategy=strategy_obj,
).run()

plot_obj = Plotter(
    backtest_results=backtest_results,
    strat_data=strategy_obj
)

plot_obj.create_dashboard(
    indicators=pd.concat([strategy_obj.fast_ma, strategy_obj.slow_ma], axis=1),
    stats=stats,
)
temp = 1
