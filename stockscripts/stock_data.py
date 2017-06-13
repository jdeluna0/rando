import pandas as pd
from pandas_datareader import data, wb

### Returns multiple pandas dataframes
def stocklist(start,end):
    d = raw_input('Enter the symbols you want to analyze separated by a space: ').split()
    a = []
    dicti = {}
    for n in d:
        b = n.lower()
        try:
            b = data.DataReader(n.upper(), "google", start, end)
        except:
            print
            print "{0} ticker not found.".format(n)
            print
            continue
        a.append(b)
        dicti[n.upper()] = b["Close"]
    stocks = pd.DataFrame(dicti)
    return stocks

### Returns a single pandas dataframe
def single(start,end):
    symbol = raw_input('Enter a single stock symbol: ')
    try:
        symbol = data.DataReader(symbol.upper(), "google", start, end)
    except:
        print
        print "{0} ticker not found.".format(symbol)
        print 
        return
    return symbol