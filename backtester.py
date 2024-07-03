import pandas as pd
import numpy as np

#based on the code given itll take the data from some api and return it as a dataframe, the split function will give the df split for testing 
#and training. Eg if you put 70 in split, it will give you a dataframe that's 70 percent the og and the other 30 will be for backtest.
#n will just be the size of the df.
def getstockdata(stockcode,split,n):
    stock_data = pd.read_csv(stockcode)
    pass


# The way this function will work is that it will iterate through the signals df, which includes a column of either buy hold or sell at each
#tick. This function will also take how much money you have as well as your maximum position(idk what it is but I think its important?)
def backtester(signalsdf, initialinvestment, maxpos):
    pass
