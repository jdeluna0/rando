#!/usr/bin/env python

import datetime
import mathmulti_functions as m
import google_intraday as g
from pcandle import pandas_candlestick_ohlc
from cur_quotes import quotes
from stock_data import stocklist,single

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


    elif opt == 'quote':
        quotes()
    else:
        print 
        print "Please choose an appropriate option."
        print

print "Bye Bye!"
