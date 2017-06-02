import pandas as pd
from pandas_datareader import data, wb #import pandas.io.data as web   Package and modules for importing data; this code may change depending on pandas version
import datetime
import matplotlib.pyplot as plt

# This line is necessary for the plot to appear in a Jupyter notebook
#%matplotlib inline
# Control the default size of figures in this Jupyter notebook
#%pylab inline
#pylab.rcParams['figure.figsize'] = (15, 9)   # Change the size of plots

start = datetime.datetime(2016,12,8)
end = datetime.date.today()

# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
slw = data.DataReader("SLW", "yahoo", start, end)
#neo = data.DataReader("NEO", "yahoo", start, end)

#type(slw)
#print slw.head()
#print
#print neo.head()

slw["Adj Close"].plot(grid = True) # Plot the adjusted closing price of AAPL
plt.show

#https://ntguardian.wordpress.com/2016/09/19/introduction-stock-market-data-python-1/
