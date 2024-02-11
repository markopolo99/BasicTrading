from backtester.strategy import Strategy
import pandas as pd

params = {
    'learning_rate': 0.2695951858961848,
    'max_depth': 113,
    'subsample': 0.8827901725394613,
    'colsample_bytree': 0.6776125588779389,
    'alpha': 41.6275162231194,
    'lambda': 36.72078927379518,
    'n_estimators': 100,
    'random_state': 42,
    'use_label_encoder': False,
    'objective': 'binary:hinge',
}


class StrategyDC(Strategy):

    def __init__(self, model, threshold_long, threshold_short, threshold_close_long, threshold_close_short, indicators):
        self.model = model
        self.threshold_long = threshold_long
        self.threshold_short = threshold_short
        self.threshold_close_long = threshold_close_long
        self.threshold_close_short = threshold_close_short
        self.indicators = indicators

    def strat_data(self, stock_info):
        self.stock_info = stock_info,

    def long(self, date):
        if date in self.indicators.index:
            current_position = self.model.predict_proba(pd.DataFrame(self.indicators.loc[date]).T)[0][1]
        else:
            return False

        if current_position > self.threshold_long:
            enter_position = True
            self.position = 'long'
        else:
            enter_position = False

        return enter_position

    def short(self, date):
        if date in self.indicators.index:
            current_position = self.model.predict_proba(pd.DataFrame(self.indicators.loc[date]).T)[0][0]
        else:
            return False

        if current_position > self.threshold_short:
            enter_position = True
            self.position = 'short'
        else:
            enter_position = False

        return enter_position

    def close(self, date):
        """
        Check to see if the moving average crosses from above
        or below.
        """
        if date in self.indicators.index:
            current_position = self.model.predict_proba(pd.DataFrame(self.indicators.loc[date]).T)[0]
        else:
            return False

        if self.position == 'long' and current_position[1] > self.threshold_close_long:
            close_position = True
        elif self.position == 'short' and current_position[0] > self.threshold_close_short:
            close_position = True
        else:
            close_position = False

        return close_position
