from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


class Plotter:

    def __init__(self, strat_data, backtest_results) -> None:
        self.data = strat_data
        self.backtest_results = backtest_results
        self.realised_equity = pd.DataFrame(backtest_results.equity.realised)
        self.unrealised_equity = pd.DataFrame(backtest_results.equity.unrealised)

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
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=self.backtest_results.tradelog.log["Exit time"],
                y=self.backtest_results.tradelog.log["Entry price"],
                mode="markers",
                name="Positions",
            ),
            row=1,
            col=1,
        )

        fig.update_layout(xaxis_rangeslider_visible=False)

        # PLOT OF INDICATOR MOVEMENTS
        for col in indicators.columns:
            fig.add_trace(
                go.Scatter(
                    x=indicators.index,
                    y=indicators[col],
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
            ),
            row=3,
            col=1,
        )

        # PLOT OF EQUITY MOVEMENT ACROSS TIME
        fig.add_trace(
            go.Scatter(
                x=self.unrealised_equity.iloc[:, 0],
                y=self.unrealised_equity.iloc[:, 1],
                mode="lines",
                name="Unrealised",
            ),
            row=1,
            col=2,
        )

        fig.add_trace(
            go.Scatter(
                x=self.realised_equity.iloc[:, 0],
                y=self.realised_equity.iloc[:, 1],
                mode="markers",
                name="Equity",
            ),
            row=1,
            col=2,
        )

        # Plots of positions
        fig.add_trace(
            go.Scatter(
                x=self.backtest_results.tradelog.log["Exit time"],
                y=self.backtest_results.tradelog.log["Spread"],
                mode="markers",
                name="Spread",
            ),
            row=4,
            col=1,
        )

        # PLOT OF TRADING STATISTICS
        fig.add_trace(
            go.Table(
                header=dict(values=["Statistics", "Values"]),
                cells=dict(values=stats.T),
            ),
            row=3,
            col=2,
        )

        fig.show()
