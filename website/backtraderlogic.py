import importlib.util
import sys
import backtrader as bt
import yfinance as yf

def load_strategy(file_path):
    spec = importlib.util.spec_from_file_location("user_strategy", file_path)
    strategy_module = importlib.util.module_from_spec(spec)
    sys.modules["user_strategy"] = strategy_module
    spec.loader.exec_module(strategy_module)
    return strategy_module.LinearRegressionStrategy

if __name__ == '__main__':
    strategy_file = "testuserstrategy.py"
    strategy_class = load_strategy(strategy_file)

    cerebro = bt.Cerebro()

    # Add the custom strategy
    cerebro.addstrategy(strategy_class)
    
    # Download data from Yahoo Finance
    nvda_data = yf.download("NVDA", start="2018-01-01", end="2018-12-31")

    # Convert data to PandasData for backtrader
    data = bt.feeds.PandasData(dataname=nvda_data)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addobserver(bt.observers.Value)

    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.plot(iplot=True, volume=False)