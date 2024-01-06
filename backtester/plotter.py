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
                name="Stock price",

            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=self.backtest_results.tradelog.log.index,
                y=self.backtest_results.tradelog.log["Entry price"],
                mode="markers",
                name="Entry price",
                marker_symbol="diamond-dot",
                marker_size=13,
                marker_line_width=2,
                marker_line_color="rgba(0,0,0,0.7)",
                marker_color="rgba(0,255,0,0.7)",
                hovertemplate="Entry Price: %{y:.2f}",

            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=self.backtest_results.tradelog.log["Exit time"],
                y=self.backtest_results.tradelog.log["Exit price"],
                mode="markers",
                name="Exit price",
                marker_symbol="diamond-dot",
                marker_size=13,
                marker_line_width=2,
                marker_line_color="rgba(0,0,0,0.7)",
                marker_color="rgba(255,0,0,0.7)",
                hovertemplate="Exit Price: %{y:.2f}",
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
                name="Volume",
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
                name="Unrealised equity",
                marker_color="blue",
            ),
            row=1,
            col=2,
        )

        fig.add_trace(
            go.Scatter(
                x=self.realised_equity.iloc[:, 0],
                y=self.realised_equity.iloc[:, 1],
                mode="markers",
                name="Realised equity",
                marker_color="red",
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
                marker_size=list(abs(self.backtest_results.tradelog.log["Spread"].values) * 10),
                marker_color=self.backtest_results.tradelog.log["Spread"].apply(lambda val: 'green' if val > 0 else 'red'),
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
