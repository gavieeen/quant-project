# user_strategy.py
import numpy as np
import backtrader as bt

class LinearRegression:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def fit(self, X, y):
        x_mean = np.mean(X)
        y_mean = np.mean(y)

        numerator = 0
        denominator = 0

        for i in range(len(X)):
            numerator += (X[i] - x_mean) * (y[i] - y_mean)
            denominator += (X[i] - x_mean) ** 2

        self.slope = numerator / denominator
        self.intercept = y_mean - (self.slope * x_mean)

    def predict(self, X):
        return self.slope * X + self.intercept

class LinearRegressionStrategy(bt.Strategy):
    params = (
        ("lookback_period", 30),
    )

    def __init__(self):
        self.lr = LinearRegression()
        self.data_close = self.datas[0].close

    def next(self):
        if len(self.data_close) > self.params.lookback_period:
            X = np.arange(0, self.params.lookback_period)
            y = np.array(self.data_close.get(size=self.params.lookback_period))

            self.lr.fit(X, y)
            predicted_price = self.lr.predict(self.params.lookback_period)

            current_price = self.data_close[0]

            if predicted_price > current_price:
                self.buy()
            elif predicted_price < current_price:
                self.sell()