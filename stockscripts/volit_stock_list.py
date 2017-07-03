import requests
from bs4 import BeautifulSoup
import google_intraday as g
import datetime
import pandas as pd

#https://www.benzinga.com/news/17/06/9669712/22-stocks-moving-in-thursdays-pre-market-session - 6/29
#https://www.benzinga.com/news/17/06/9675719/22-stocks-moving-in-fridays-pre-market-session - 6/30
#https://www.benzinga.com/news/17/07/9681342/22-stocks-moving-in-mondays-pre-market-session - 7/3




def get_tickers(parsed_html):
	a = []
	for div in soup.findAll('a', attrs={'class':'ticker'}):
		a.append(div.contents[0])
	return a



def get_intraday_data(ticker):
	q = g.GoogleIntradayQuote(ticker,300,3)
	count = 0
	for entry in q.date:
		if entry == datetime.date(2017, 6, 29):
			count += 1

	dict_list = []
	#dict_list = [{'ticker':ticker,'date':str(q.date[0]),'time':str(q.time[0]),'open':q.open_[0],'high':q.high[0],'low':q.low[0],'close':q.close[0],'volume':q.volume[0]}]
	for i in range(0, count):
		dict_list.append({'ticker':ticker,'date':str(q.date[i]),'time':str(q.time[i]),'open':q.open_[i],'high':q.high[i],'low':q.low[i],'close':q.close[i],'volume':q.volume[i]})
	df = pd.DataFrame(dict_list, columns=['ticker','date','time','open','high','low','close','volume'])
	return df


r = requests.get('https://www.benzinga.com/news/17/06/9669712/22-stocks-moving-in-thursdays-pre-market-session') 
soup = BeautifulSoup(r.content, 'html.parser')
ticker_list = get_tickers(soup)

dataframe_list = []
for symbol in ticker_list:
	dataframe_list.append(get_intraday_data(symbol))
print dataframe_list
