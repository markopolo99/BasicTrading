import sys
import optuna
import pickle

from backtester.data import LoadData, StockData
from backtester.backtester import Backtester
from backtester.plotter import Plotter

from strategies.strat_crossover.strategy_crossover import StrategyDC

sys.path.append("C:\\Users\\tomic\\Desktop\\BasicStrategy\\BasicTrading")

# Specify the type of data you want
ticker = 'DKNG'  # 'NET', 'UPST', 'U'
granul = '1h'
start = '2022-03-01'
end = '2024-01-20'

# Load data according to specifications
df_prices = LoadData(
    ticker=ticker,
    granularity=granul,
    start_date=start,
    end_date=end,).df_prices

with open("xgb_model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

with open("indicators.pkl", "rb") as f:
    indicators = pickle.load(f)


def objective(trial):
    threshold_long = trial.suggest_float('threshold_long', 0.5, 1)
    threshold_short = trial.suggest_float('threshold_short', 0.5, 1)
    threshold_close_long = trial.suggest_float('threshold_close_long', 0.5, 1)
    threshold_close_short = trial.suggest_float('threshold_close_short', 0.5, 1)

    stock_obj = StockData(df_prices)

    strategy_obj = StrategyDC(
        model=loaded_model,
        threshold_long=threshold_long,
        threshold_short=threshold_short,
        threshold_close_long=threshold_close_long,
        threshold_close_short=threshold_close_short,
        indicators=indicators
    )

    returns = Backtester(
        stock=stock_obj,
        strategy=strategy_obj,
    ).run(optimizing=True)

    if returns['train_set'][0].sum()[0] != 0:
        equity = returns['train_set'][0]['equity'][-1]
    else:
        equity = 0

    return equity


study = optuna.create_study(
    directions=['maximize'],
    storage="sqlite:///db.sqlite3",
    study_name="XGB model run #3",
    load_if_exists=True,
)

study.optimize(objective, n_trials=100)


best_params = {'threshold_long': 0.717619207568592, 'threshold_short': 0.9283008644109811, 'threshold_close_long': 0.7210653208474397, 'threshold_close_short': 0.6222695425371303}
# best_params = study.best_params
stock_obj = StockData(df_prices)

strategy_obj = StrategyDC(
    model=loaded_model,
    indicators=indicators,
    **best_params,
)

train_test_info, returns = Backtester(
    stock=stock_obj,
    strategy=strategy_obj,
).run(optimizing=False)


for dataset in ['train', 'test', 'validation']:

    strategy_obj.strat_data(getattr(stock_obj, dataset))

    plot_obj = Plotter(
        backtest_results=train_test_info[dataset]['trade_positions_' + dataset],
        strat_data=strategy_obj,
        equity=train_test_info[dataset]['equity_' + dataset],
    )

    plot_obj.create_dashboard(
        indicators=indicators,
        stats=train_test_info[dataset]['stats_' + dataset],
    )
