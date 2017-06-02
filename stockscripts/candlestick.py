#!/usr/bin/env python
import pandas as pd
import numpy as np
from pandas_datareader import data, wb #import pandas.io.data as web   Package and modules for importing data; this code may change depending on pandas version
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY, date2num
from matplotlib.finance import candlestick_ohlc
import urllib2
 
def pandas_candlestick_ohlc(dat, stick = "day", otherseries = None):
    """
    :param dat: pandas DataFrame object with datetime64 index, and float columns "Open", "High", "Low", and "Close", likely created via DataReader from "yahoo"
    :param stick: A string or number indicating the period of time covered by a single candlestick. Valid string inputs include "day", "week", "month", and "year", ("day" default), and any numeric input indicates the number of trading days included in a period
    :param otherseries: An iterable that will be coerced into a list, containing the columns of dat that hold other series to be plotted as lines
 
    This will show a Japanese candlestick plot for stock data stored in dat, also plotting other series if passed.
    """
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    dayFormatter = DateFormatter('%d')      # e.g., 12
 
    # Create a new DataFrame which includes OHLC data for each period specified by stick input
    transdat = dat.loc[:,["Open", "High", "Low", "Close"]]
    if (type(stick) == str):
        if stick == "day":
            plotdat = transdat
            stick = 1 # Used for plotting
        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) # Identify weeks
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) # Identify months
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) # Identify years
            grouped = transdat.groupby(list(set(["year",stick]))) # Group by year and other appropriate variable
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                            "High": max(group.High),
                                            "Low": min(group.Low),
                                            "Close": group.iloc[-1,3]},
                                           index = [group.index[0]]))
            if stick == "week": stick = 5
            elif stick == "month": stick = 30
            elif stick == "year": stick = 365
 
    elif (type(stick) == int and stick >= 1):
        transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                        "High": max(group.High),
                                        "Low": min(group.Low),
                                        "Close": group.iloc[-1,3]},
                                       index = [group.index[0]]))
 
    else:
        raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')
 
 
    # Set plot parameters, including the axis object ax used for plotting
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)
 
    ax.grid(True)
 
    # Create the candelstick chart
    candlestick_ohlc(ax, list(zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
                      plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                      colorup = "black", colordown = "red", width = stick * .4)
 
    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)
 
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
 
    plt.show()
 
#MOVING AVERAGES - CROSSING SIGNALS A POSSIBLE CHANGE IN TREND
#function takes a data object 
def move_avg(symbol):
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
    stock_change = stocks.apply(lambda x: np.log(x) - np.log(x.shift(1))) # shift moves dates back by 1.
    stock_change.plot(grid = True).axhline(y = 0, color = "black", lw = 2)
    plt.show()

#SHOWS STOCK PRICES OF THE STOCK DATAFRAME
def prices(stocks):
    stocks.plot(secondary_y = ["SLW","MSFT"],grid = True )
    plt.show()

def stocklist():
    d = raw_input('Enter the symbols you want to analyze separated by a space: ').split()
    a = []
    dicti = {}
    for n in d:
        b = n.lower()
        b = data.DataReader(n.upper(), "google", start, end)
        a.append(b)
        dicti[n.upper()] = b["Close"]
    stocks = pd.DataFrame(dicti)
    return stocks

def single():
    symbol = raw_input('Enter a single stock symbol: ')
    symbol = data.DataReader(symbol.upper(), "google", start, end)
    return symbol

#RETURNS INTRADAY DATA
def get_google_data(symbol, period, window):
    url_root = 'http://finance.google.com/finance/info?client=ig&q='
    url_root += str(period) + '&p=' + str(window)
    url_root += 'd&f=d,o,h,l,c,v&df=cpct&q=' + symbol
    response = urllib2.urlopen(url_root)
    data = response.read().split('\n')
    #actual data starts at index = 7
    #first line contains full timestamp,
    #every other line is offset of period from timestamp
    parsed_data = []
    anchor_stamp = ''
    end = len(data)
    for i in range(7, end):
        cdata = data[i].split(',')
        if 'a' in cdata[0]:
            #first one record anchor timestamp
            anchor_stamp = cdata[0].replace('a', '')
            cts = int(anchor_stamp)
        else:
            try:
                coffset = int(cdata[0])
                cts = int(anchor_stamp) + (coffset * period)
                parsed_data.append((dt.datetime.fromtimestamp(float(cts)), float(cdata[1]), float(cdata[2]), float(cdata[3]), float(cdata[4]), float(cdata[5])))
            except:
                pass # for time zone offsets thrown into data
    df = pd.DataFrame(parsed_data)
    df.columns = ['ts', 'o', 'h', 'l', 'c', 'v']
    df.index = df.ts
    del df['ts']
    return df

###################
# MAIN CODE LOGIC #
###################

choose_date = raw_input('Date to begin data collection in the format MM DD YYYY: ')
date_list = [int(n) for n in choose_date.split()]
start = datetime.datetime(date_list[2],date_list[0],date_list[1])
end = datetime.date.today()

while True: 

    print '\n\t','Single Stock Analysis' '\n\t', 'Candlestick: C', \
    '\n\t','Moving Average: A', '\n\t', 'Intraday: I', '\n\n\t', 'Multiple Stock Analysis', \
    '\n\t', 'Stock Return: R', '\n\t', 'Price Change(%): L', '\n\t', \
    'Prices(chart): P'
    analz = raw_input('Select an option, q to quit: ')	
	
    if analz == 'q' or analz == 'Q':
        break
    if analz == 'A':
        symbol = single()
        move_avg(symbol)
    if analz == 'R':
        stocks = stocklist()
        stock_return(stocks)
    if analz == 'L':
        stocks = stocklist()
        log_price(stocks)
    if analz == 'P':
        stocks = stocklist()
        prices(stocks)
    if analz == 'C':
        symbol = single()
        pandas_candlestick_ohlc(symbol)
    if analz == 'I':
        symbol = raw_input('Enter a single stock symbol: ').upper()
        interval = raw_input('Choose number of days to analyze and a time interval in seconds(DD SS): ').split()
        spread = get_google_data(symbol,300,10)
        f = raw_input('Choose number of entries to analyze: ')
        f = int(f)
        print spread.head(f)

print "Bye Bye!"
