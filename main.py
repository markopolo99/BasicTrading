from utility.load_data import load_data
from utility.make_plots import *

from strategies.moving_average_crossover import MACrossover
import matplotlib.pyplot as plt

# Load historical data for portfolio
df = load_data(start_date="2023-01-01", ticker="U", granularity="1h")

ma_object = MACrossover(
    df_prices=df["close"], 
    ma_range=range(3,20),
)

mv_positions = ma_object.moving_avg_calc()

# Plot data
plot_positions(mv_positions, df["close"])


