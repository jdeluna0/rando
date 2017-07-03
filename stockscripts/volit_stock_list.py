import requests
from bs4 import BeautifulSoup
import google_intraday as g
import datetime
#https://www.benzinga.com/news/17/06/9669712/22-stocks-moving-in-thursdays-pre-market-session - 6/29
#https://www.benzinga.com/news/17/06/9675719/22-stocks-moving-in-fridays-pre-market-session - 6/30
#https://www.benzinga.com/news/17/07/9681342/22-stocks-moving-in-mondays-pre-market-session - 7/3


r = requests.get('https://www.benzinga.com/news/17/06/9669712/22-stocks-moving-in-thursdays-pre-market-session') 
soup = BeautifulSoup(r.content, 'html.parser')


#for div in soup.findAll('a', attrs={'class':'ticker'}):
#	ticker = div.contents[0]
#	q = g.GoogleIntradayQuote(ticker,300,3)
#	for i in q.date:
#		if i == datetime.date(2017, 6, 29):
#			print q.date[i],q.time[i],q.open_[i],q.high[i],q.low[i],q.close[i],q.volume[i]


q = g.GoogleIntradayQuote('SGYP',300,3)
for i in q.date:
	if i == datetime.date(2017, 6, 29):




#		print q.date[i],q.time[i],q.open_[i],q.high[i],q.low[i],q.close[i],q.volume[i]