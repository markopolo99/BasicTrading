# import sys
# sys.path.append("C:\\Users\\tomic\\Desktop\\BasicStrategy\\BasicTrading")

import cProfile
import pstats
import pandas as pd

from backtester.data import LoadData, StockData
from backtester.backtester import Backtester
from backtester.plotter import Plotter

from strategies.strategy_crossover import StrategyDC

# Specify the type of data you want
ticker = 'DKNG'
granul = '1h'
start = '2022-03-01'
end = '2024-01-20'

# Load data according to specifications
df_prices = LoadData(
    ticker=ticker,
    granularity=granul,
    start_date=start,
    end_date=end,).df_prices

stock_obj = StockData(df_prices)

strategy_obj = StrategyDC(
    window_fast=5,
    window_slow=10,
)


train_test_info = Backtester(
    stock=stock_obj,
    strategy=strategy_obj,
).run()

cProfile.run('Backtester(stock=stock_obj,strategy=strategy_obj,).run()', 'profile_results')
profile_stats = pstats.Stats('profile_results')
profile_stats.sort_stats('cumtime').print_stats(20)

plot_obj = Plotter(
    # backtest_results=backtest_results,
    strat_data=strategy_obj,
    # equity=equity,

)

plot_obj.create_dashboard(
    indicators=pd.concat([strategy_obj.fast_ma, strategy_obj.slow_ma], axis=1),
    # stats=stats,
)
temp = 1
