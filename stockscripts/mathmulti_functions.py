#MOVING AVERAGES - CROSSING SIGNALS A POSSIBLE CHANGE IN TREND
#function takes a single data object 
import matplotlib.pyplot as plt

def move_avg(symbol, end):
    import numpy as np
    from pcandle import pandas_candlestick_ohlc

    symbol["20d"] = np.round(symbol["Close"].rolling(window = 20, center = False).mean(), 2)
    symbol["50d"] = np.round(symbol["Close"].rolling(window = 50, center = False).mean(), 2)
    symbol["200d"] = np.round(symbol["Close"].rolling(window = 200, center = False).mean(), 2)
    pandas_candlestick_ohlc(symbol.loc['2016-01-04':end,:], otherseries = ["20d", "50d", "200d"])
    #pandas_candlestick_ohlc(symbol.loc['2016-06-04':'2016-12-15',:], otherseries = ["20d", "50d", "200d"])
    plt.show()
#graphs stock return since beginning of the period of interest
def stock_return(stocks):

    sreturn = stocks.apply(lambda x: x / x[0])
    sreturn.plot(grid = True).axhline(y = 1, color = "black", lw = 2)
    plt.show()

#MAPPING CHANGES IN PRICE VIA LOG - REPRESENTS THE PERCENTAGE CHANGE IN A STOCK PER DAY
#function take a dataframe arg
def log_price(stocks):
    import numpy as np

    stock_change = stocks.apply(lambda x: np.log(x) - np.log(x.shift(1))) # shift moves dates back by 1.
    stock_change.plot(grid = True).axhline(y = 0, color = "black", lw = 2)
    plt.show()

#SHOWS STOCK PRICES OF THE STOCK DATAFRAME
def prices(stocks):

    stocks.plot(secondary_y = ["MSFT","NEO"],grid = True )
    plt.show()