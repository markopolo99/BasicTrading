from utility.load_data import load_data
from utility.make_plots import *

from strategies.mean_reversion import MeanReversion
from strategies.moving_average_crossover import MACrossover

# Load historical data for portfolio
df = load_data(start_date="2023-07-01", ticker="U", granularity="1h")

# # Test mean reversion strat
# ma_object = MeanReversion(
#     df_prices=df["close"], 
#     window=30,
# )

# mv_positions = ma_object.run_simulation()
fast_range = range(20)
slow_range = range(80)

returns = pd.DataFrame(index=slow_range, columns=fast_range)

for fast in fast_range:
    for slow in slow_range:
        if fast < slow:
            ma_object = MACrossover(
                df_prices=df["close"], 
                ma_pair=[fast, slow],
            )

            ma_object.get_positions()
            ma_object.get_returns()

            returns.iloc[slow, fast] = ma_object.trades["return"].sum()

max_value_location = returns.stack().idxmax()

# Plot data
ma_object = MACrossover(
    df_prices=df["close"], 
    ma_pair=[8, 40],
)

ma_object.get_positions()
ma_object.get_returns()

plot_positions(ma_object.positions, df["close"])


