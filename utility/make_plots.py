import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_prices(df: pd.DataFrame) -> None:

    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Plot the available data
    ax.plot(df.index, df)

    # Set the date locator to skip missing dates
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    
    # Format the date ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    plt.show()

    pass

def plot_positions(df_positions: pd.DataFrame, df_prices: pd.DataFrame) -> None:

    # Create the main plot
    fig, ax1 = plt.subplots()

    # Plot the first dataset with the first y-axis
    ax1.plot(df_prices, color='tab:blue')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Close prices', color='tab:blue')

    # Create a second y-axis and plot the second dataset
    ax2 = ax1.twinx()
    ax2.plot(df_positions, color='tab:red')
    ax2.set_ylabel('Position', color='tab:red')

    pass
