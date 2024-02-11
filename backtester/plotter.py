from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


class Plotter:

    def __init__(self, strat_data, backtest_results, equity) -> None:
        self.data = strat_data
        self.backtest_results = backtest_results
        self.equity = equity

    def create_dashboard(self, indicators, stats):

        fig = make_subplots(
            rows=4,
            cols=2,
            specs=[
                [{}, {"rowspan": 2}],
                [{}, None],
                [{}, {"type": "table", "rowspan": 2}],
                [{}, None]],
            shared_xaxes=True,
        )

        # PLOT OF STOCK PRICES AS CANDLESTICKS
        fig.add_trace(
            go.Candlestick(
                x=self.data.stock_info[0].index,
                open=self.data.stock_info[0].open,
                high=self.data.stock_info[0].high,
                low=self.data.stock_info[0].low,
                close=self.data.stock_info[0].close,
                name="Stock price",

            ),
            row=1,
            col=1,
        )

        for pos in self.backtest_results.iterrows():
            if pos[1].position_type == 'long':
                fig.add_trace(
                    go.Scatter(
                        x=[pos[1].entry_time, pos[1].exit_time],
                        y=[pos[1].entry_price, pos[1].exit_price],
                        mode="lines+markers",
                        name="Entry price",
                        marker_color='green'
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=[pos[1].entry_time, pos[1].exit_time],
                        y=[pos[1].entry_price, pos[1].exit_price],
                        mode="lines+markers",
                        name="Entry price",
                        marker_color='red'
                    ),
                    row=1,
                    col=1,
                )

        fig.update_layout(xaxis_rangeslider_visible=False)

        # PLOT OF INDICATOR MOVEMENTS
        for col in range(indicators.shape[1]):

            fig.add_trace(
                go.Scatter(
                    x=indicators.index,
                    y=indicators.iloc[:, col],
                    mode="lines",
                    name=col,
                ),
                row=2,
                col=1,
            )

        # PLOT OF VOLUME AT EACH POINT IN TIME
        fig.add_trace(
            go.Bar(
                x=self.data.stock_info[0].index,
                y=self.data.stock_info[0].volume,
                marker_color='blue',
                name="Volume",
            ),
            row=3,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=self.equity.index,
                y=self.equity.equity,
                mode="lines+markers",
                name="Realised equity",
                marker_color="yellow",
                marker_line_color="red"
            ),
            row=1,
            col=2,
        )

        # Plots of positions
        fig.add_trace(
            go.Scatter(
                x=self.backtest_results.exit_time,
                y=self.backtest_results.spread,
                mode="markers",
                name="Spread",
                marker_size=list(abs(self.backtest_results.spread) * 10),
                marker_color=self.backtest_results.spread.apply(lambda val: 'green' if val > 0 else 'red'),
            ),
            row=4,
            col=1,
        )

        # PLOT OF TRADING STATISTICS
        fig.add_trace(
            go.Table(
                header=dict(values=["Statistics", "Values"]),
                cells=dict(values=pd.DataFrame(stats.items()).T),

            ),
            row=3,
            col=2,
        )

        fig.show()
