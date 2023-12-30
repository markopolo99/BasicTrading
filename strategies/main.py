from backtester.data import LoadData, StockData
from backtester.backtester import Backtester

from strategies.strategy_crossover import StrategyDC
import sys
sys.path.append("C:\\Users\\tomic\\Desktop\\BasicStrategy\\BasicTrading")

# Specify the type of data you want
ticker = 'DKNG'
granul = '1h'
start = '2022-01-01'
end = '2023-12-01'

# Load data according to specifications
df_prices = LoadData(
    ticker=ticker,
    granularity=granul,
    start_date=start,
    end_date=end,).df_prices

stock_obj = StockData(df_prices)

backtest_obj = Backtester(stock_obj, StrategyDC)
