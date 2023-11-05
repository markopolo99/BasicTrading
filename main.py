from utility.load_data import load_data
from utility.make_plots import *

from strategies.mean_reversion import MeanReversion
from strategies.moving_average_crossover import MACrossover
import matplotlib.pyplot as plt

# Load historical data for portfolio
df = load_data(start_date="2023-07-01", ticker="U", granularity="1h")

# # Test mean reversion strat
# ma_object = MeanReversion(
#     df_prices=df["close"], 
#     window=30,
# )

# mv_positions = ma_object.run_simulation()


ma_object = MACrossover(
    df_prices=df["close"], 
    ma_pair=[4,15],
)

ma_object.get_positions()
ma_object.get_returns()

# Plot data
plot_positions(ma_object.positions, df["close"])


