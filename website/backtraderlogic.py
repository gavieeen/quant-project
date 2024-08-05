import importlib.util
import sys
import backtrader as bt
import yfinance as yf
import os
import tempfile
import ast

def load_strategy(file_content):
    file_path = '/tmp/temp_algorithm.py'
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    spec = importlib.util.spec_from_file_location("strategy_module", file_path)
    strategy_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(strategy_module)
    os.remove(file_path)  # Clean up the temporary file
    return strategy_module.MyStrategy 

def run_algorithm(file_content):
    
   # Execute the uploaded code
    exec(file_content, globals())
    
    # Parse the file content to find the strategy class
    strategy_class_name = None
    parsed_code = ast.parse(file_content)
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Attribute) and base.attr == 'Strategy':
                    strategy_class_name = node.name
                    break
            if strategy_class_name:
                break

    if strategy_class_name is None:
        raise ValueError("No valid strategy class found in the uploaded file.")

    strategy_class = globals().get(strategy_class_name)
    if not strategy_class:
        raise ValueError(f"Strategy class {strategy_class_name} not found in global scope.")

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy_class)
    
    # Download data from Yahoo Finance
    nvda_data = yf.download("NVDA", start="2018-01-01", end="2018-12-31")

    # Convert data to PandasData for backtrader
    data = bt.feeds.PandasData(dataname=nvda_data)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addobserver(bt.observers.Value)
    start = cerebro.broker.getvalue()
    #print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    ending = cerebro.broker.getvalue()
    #print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
    plot = cerebro.plot(iplot=True, volume=False)
    return start, ending, plot