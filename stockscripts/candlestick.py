#!/usr/bin/env python

from pcandle import pandas_candlestick_ohlc
import mathmulti_functions as m
import datetime
import pandas as pd
from pandas_datareader import data, wb
 
### Returns multiple pandas dataframes
def stocklist():
    d = raw_input('Enter the symbols you want to analyze separated by a space: ').split()
    a = []
    dicti = {}
    for n in d:
        b = n.lower()
        try:
            b = data.DataReader(n.upper(), "google", start, end)
        except:
            print
            print "{0} ticket not found.".format(n)
            print
            continue
        a.append(b)
        dicti[n.upper()] = b["Close"]
    stocks = pd.DataFrame(dicti)
    return stocks

### Returns a single pandas dataframe
def single():
    symbol = raw_input('Enter a single stock symbol: ')
    try:
        symbol = data.DataReader(symbol.upper(), "google", start, end)
    except:
        print
        print "{0} ticket not found.".format(symbol)
        print 
        return
    return symbol


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
    opt = raw_input('Select an option, q to quit: ')	
	
    if opt == 'q' or opt == 'Q':
        break
    elif opt == 'A':
        symbol = single()
        m.move_avg(symbol, end)
    elif opt == 'R':
        stocks = stocklist()
        m.stock_return(stocks)
    elif opt == 'L':
        stocks = stocklist()
        m.log_price(stocks)
    elif opt == 'P':
        stocks = stocklist()
        m.prices(stocks)
    elif opt == 'C':
        symbol = single()
        pandas_candlestick_ohlc(symbol)
    elif opt == 'I':
        symbol = raw_input('Enter a single stock symbol: ').upper()
        interval = raw_input('Choose number of days to analyze and a time interval in seconds(DD SS): ').split()
        spread = get_google_data(symbol,300,10)
        f = raw_input('Choose number of entries to analyze: ')
        f = int(f)
        print spread.head(f)
    else:
        print 
        print "Please choose an appropriate option."
        print

print "Bye Bye!"
