#!/usr/bin/env python

def quotes():
    from googlefinance import getQuotes

    stocklist = raw_input('Enter stocks for current quote: ').split()

    print
    print "{0}   {1}   {2}".format('Stock Symbol', 'Last Trade Price', 'Last Trade Time')
    for stock in stocklist:
        try:
            quote = getQuotes([stock])[0]
        except:
            print
            print "{0} not found.".format(stock)
            print
            exit()
        print "{0:14} {1:>16} {2:>17}".format(quote['StockSymbol'],quote['LastTradePrice'],quote['LastTradeTime'])
    print
