import xgboost
import optuna
import pickle

import pandas as pd
import numpy as np
from backtester.data import LoadData
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import sys
sys.path.append("C:\\Users\\tomic\\Desktop\\BasicStrategy\\BasicTrading")


class TechnicalAnalysis:

    def __init__(self, prices) -> None:
        self.prices = prices
        self.indicator = pd.DataFrame(index=prices.index)

    def moving_average(self):
        """
        Create a lot of combinations of moving averages
        as percentage changes
        """
        for i in range(50, 5):
            for j in range(100, 5):
                if j > i:
                    ma_i = self.prices.open.rolling(window=i).mean()
                    ma_j = self.prices.open.rolling(window=j).mean()

                    self.indicator['ma_' + str(i) + '_' + str(j)] = ma_i / ma_j

    def resistance(self, threshold_support=0.02, threshold_resistance=0.02):
        """
        Find the percentage difference of the highest
        high and lowest lower of the past 'x' hours
        """

        for period in range(200, 1000, 100):

            support = self.prices.open.rolling(window=period).min() * (1 + threshold_support)
            resistance = self.prices.open.rolling(window=period).max() * (1 - threshold_resistance)

            self.indicator['support_' + str(period)] = (self.prices.open - support) / support
            self.indicator['resistance_' + str(period)] = (self.prices.open - resistance) / resistance

    def volatility(self):
        """
        Find the volatility of the last 'x' periods
        """

        log_returns = np.log(self.prices.open / self.prices.open.shift(1))

        for period in range(5, 100, 5):
            self.indicator['volatility_' + str(period)] = log_returns.rolling(window=period).std()

    def volume(self):
        """
        Look at the percentage change in volume traded
        in the past 'x' hours.
        """

        for period in range(5, 100, 5):
            self.indicator['volume_' + str(period)] = self.prices.volume.pct_change(period)

    def construct_indicators(self):
        self.moving_average()
        self.resistance()
        self.volatility()
        self.volume()

        self.indicator = self.indicator.dropna()

        return self.indicator


def objective(trial):
    # Define hyperparameters to be optimized
    params = {
        'objective': 'binary:logistic',
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'max_depth': trial.suggest_int('max_depth', 3, 160),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('alpha', 1e-4, 1e2),
        'reg_lambda': trial.suggest_float('lambda', 1e-4, 1e2),
        'n_estimators': 100,
        'random_state': 42,
        'use_label_encoder': False
    }

    # Train XGBoost model
    model = xgboost.XGBClassifier(**params)

    scores = cross_val_score(model, x_train, y_train, cv=5, error_score='raise')

    return round(scores.mean(), 4)


# Specify the type of data you want
ticker = 'DKNG'  # 'NET', 'UPST', 'U'
granul = '1h'
start = '2022-03-01'
end = '2024-01-20'

# Load data according to specifications
df_prices = LoadData(
    ticker=ticker,
    granularity=granul,
    start_date=start,
    end_date=end,).df_prices

ta_obj = TechnicalAnalysis(
    prices=df_prices
)

indicators = ta_obj.construct_indicators()
indicators.replace([np.inf, -np.inf], np.nan, inplace=True)
indicators.dropna(inplace=True)

# We are only going to try predict an upward or
# downward movement
price_move = (df_prices.open.pct_change() > 0).astype(int)

intersection = indicators.index.intersection(price_move.index)
price_move = price_move.loc[intersection].astype(int)
indicators = indicators.loc[intersection].astype(float)

with open("indicators.pkl", "wb") as f:
    pickle.dump(indicators, f)

# Split into a train and test set
x_train, x_test, y_train, y_test = train_test_split(indicators, price_move, test_size=0.4, random_state=42)

# Optimize hyperparameters using Optuna
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)

# Check model performance out of sample
params = {
    'learning_rate': 0.21182969817990444,
    'max_depth': 109,
    'subsample': 0.9111050226952724,
    'colsample_bytree': 0.9480182261114857,
    'alpha': 23.987794200211734,
    'lambda': 13.52510737279978,
    'n_estimators': 100,
    'random_state': 42,
    'use_label_encoder': False,
    'objective': 'binary:logistic',
}

model = xgboost.XGBClassifier(**params)
model.fit(x_train, y_train)
predictions = model.predict(x_test)

accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

conf_matrix = confusion_matrix(y_test, predictions)
print("Confusion Matrix:\n", conf_matrix)

# Generate classification report
class_report = classification_report(y_test, predictions)

with open("xgb_model.pkl", "wb") as f:
    pickle.dump(model, f)
