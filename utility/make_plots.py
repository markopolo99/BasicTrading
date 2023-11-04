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