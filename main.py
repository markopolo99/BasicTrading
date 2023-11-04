from utility.load_data import load_data
from utility.make_plots import *

from strategies.mean_reversion import MeanReversion

import matplotlib.pyplot as plt

# Load historical data for portfolio
df = load_data(start_date="2023-01-01", ticker="U", granularity="1h")

mv_object = MeanReversion(
    df_prices=df["close"], 
    window=60,
)

mv_positions = mv_object.run_simulation()

# Plot data
plot_positions(mv_positions, df["close"])


