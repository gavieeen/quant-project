import importlib.util
import sys
import backtrader as bt
import yfinance as yf
import os
import tempfile
import ast
import matplotlib
matplotlib.use('Agg') # non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    ending = cerebro.broker.getvalue()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

    # Use Matplotlib directly to save the plot
    # fig=plt.figure()
    # plt.savefig(plot_file) # plt directly instead of cerebro.plot()
    # plt.show()
    plot_file = 'static/plot.png'
    # cerebro.plot()[0][0].savefig(plot_file)
    
    return start, ending, plot_file

# def generate_custom_plot(cerebro_instance, plot_file):
#     # Extract data from cerebro instance
#     data = cerebro_instance.datas
#     times = [bt.num2date(x) for x in data[0]]
#     close_prices = [x for x in data[0].close]
#     strategy_prices = [x for x in data[0].strategy_price]
#     profit_losses = [x for x in data[0].profit_loss]

#     # Create a figure and axis
#     fig, ax = plt.subplots(figsize=(12, 6))

#     # Plot the close prices
#     ax.plot(times, close_prices, label='Close Price', color='blue')
#     ax.plot(times, strategy_prices, label='Strategy Price', color='green')
#     ax.plot(times, profit_losses, label='Profit/Loss', color='red')

#     # Formatting
#     ax.set_xlabel('Date')
#     ax.set_ylabel('Price')
#     ax.set_title('Close Price over Time')
#     ax.legend()
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#     ax.xaxis.set_major_locator(mdates.MonthLocator())
#     ax.grid(True)
#     plt.xticks(rotation=45)

#     # Save the figure
#     plt.tight_layout()
#     plt.savefig(plot_file)
#     plt.close(fig)

# test_file = '../testuserstrategy.py'
# run_algorithm(open(test_file).read())