#!/usr/bin/env python

import datetime
import mathmulti_functions as m
import google_intraday as g
from MACross import Strategy, MovingAverageCrossStrategy, Portfolio, MarketOnClosePortfolio
from pcandle import pandas_candlestick_ohlc
from cur_quotes import quotes
from stock_data import stocklist,single
from pandas_datareader import data, wb

def init_dates():
    choose_date = raw_input('Date to begin data collection in the format MM DD YYYY: ')
    date_list = [int(n) for n in choose_date.split()]
    start = datetime.datetime(date_list[2],date_list[0],date_list[1])
    end = datetime.date.today()
    return start,end


###################
# MAIN CODE LOGIC #
###################

while True: 

    print '\n\t','Get a price quote: quote','\n\t','\n\t','\n\t','Single Stock Analysis' '\n\t', 'Candlestick: C', \
    '\n\t','Moving Average: A', '\n\t', 'Intraday: I', '\n\n\t', 'Multiple Stock Analysis', \
    '\n\t', 'Stock Return: R', '\n\t', 'Price Change(%): L', '\n\t', \
    'Prices(chart): P'
    opt = raw_input('Select an option, q to quit: ')	
	
    if opt == 'q' or opt == 'Q':
        break
    # Single Stock Analysis
    elif opt == 'C':
        tup = init_dates()
        start = tup[0]
        end = tup[1]
        symbol = single(start,end)
        pandas_candlestick_ohlc(symbol)
    elif opt == 'A':
        tup = init_dates()
        start = tup[0]
        end = tup[1]
        symbol = single(start,end)
        m.move_avg(symbol, end)
    elif opt == 'I':
        g.gather_data()
    
    # Multiple Stock Analysis
    elif opt == 'R':
        tup = init_dates()
        start = tup[0]
        end = tup[1]
        stocks = stocklist(start,end)
        m.stock_return(stocks)
    elif opt == 'L':
        tup = init_dates()
        start = tup[0]
        end = tup[1]
        stocks = stocklist(start,end)
        m.log_price(stocks)
    elif opt == 'P':
        tup = init_dates()
        start = tup[0]
        end = tup[1]
        stocks = stocklist(start,end)
        m.prices(stocks)
    elif opt == 'CO':
        tup = init_dates()
        start = tup[0]
        end = tup[1]
        symbol = 'AMZN'
        bars = data.DataReader(symbol, "google", start, end)
        # Create a Moving Average Cross Strategy instance 
        # with short and long moving average windows
        mac = MovingAverageCrossStrategy(symbol, bars, short_window=40, long_window=100)
        signals = mac.generate_signals()
        # Create a portfolio of AMZN, with $100,000 initial capital
        portfolio = MarketOnClosePortfolio(symbol, bars, signals, initial_capital=100000.0)
        returns = portfolio.backtest_portfolio()
        # Plot two charts to assess trades and equity curve
        fig = plt.figure()
        fig.patch.set_facecolor('white')     # Set the outer colour to white
        ax1 = fig.add_subplot(211,  ylabel='Price in $')
        # Plot the AMZN closing price overlaid with the moving averages
        bars['Close'].plot(ax=ax1, color='r', lw=2.)
        signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)
        # Plot the "buy" trades against AMZN
        ax1.plot(signals.ix[signals.positions == 1.0].index, 
                 signals.short_mavg[signals.positions == 1.0],
                 '^', markersize=10, color='m')
        # Plot the "sell" trades against AMZN
        ax1.plot(signals.ix[signals.positions == -1.0].index, 
                 signals.short_mavg[signals.positions == -1.0],
                 'v', markersize=10, color='k')
        # Plot the equity curve in dollars
        ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
        returns['total'].plot(ax=ax2, lw=2.)
        # Plot the "buy" and "sell" trades against the equity curve
        ax2.plot(returns.ix[signals.positions == 1.0].index, 
                 returns.total[signals.positions == 1.0],
                 '^', markersize=10, color='m')
        ax2.plot(returns.ix[signals.positions == -1.0].index, 
                 returns.total[signals.positions == -1.0],
                 'v', markersize=10, color='k')
        # Plot the figure
        fig.show()
    elif opt == 'quote':
        quotes()
    else:
        print 
        print "Please choose an appropriate option."
        print

print "Bye Bye!"
