import requests
from bs4 import BeautifulSoup
import google_intraday as g
from datetime import date,timedelta
import pandas as pd

#url_string = 'https://www.benzinga.com/news/17/06/9669712/22-stocks-moving-in-thursdays-pre-market-session' # 6/29
#url_string = 'https://www.benzinga.com/news/17/06/9675719/22-stocks-moving-in-fridays-pre-market-session' # 6/30
url_string = 'https://www.benzinga.com/news/17/07/9681342/22-stocks-moving-in-mondays-pre-market-session' # 7/3


date_posted = date(2017, 6, 29)
todate = date.today()
daygenerator = (date_posted + timedelta(x + 1) for x in xrange((todate - date_posted).days))
diff_days = sum(1 for day in daygenerator if day.weekday() < 5) 

def get_tickers(parsed_html):
	a = []
	for div in parsed_html.findAll('a', attrs={'class':'ticker'}):
		a.append(div.contents[0])
	return a



def get_intraday_data(ticker):
	q = g.GoogleIntradayQuote(ticker,300,diff_days) # Last value determines how many days to go back
	count = 0
	for entry in q.date:
		if entry == date_posted:
			count += 1
	dict_list = []
	#dict_list = [{'ticker':ticker,'date':str(q.date[0]),'time':str(q.time[0]),'open':q.open_[0],'high':q.high[0],'low':q.low[0],'close':q.close[0],'volume':q.volume[0]}]
	for i in range(0, count):
		dict_list.append({'ticker':ticker,'date':str(q.date[i]),'time':str(q.time[i]),'open':q.open_[i],'high':q.high[i],'low':q.low[i],'close':q.close[i],'volume':q.volume[i]})
	df = pd.DataFrame(dict_list, columns=['ticker','date','time','open','high','low','close','volume'])
	return df


r = requests.get(url_string) 
soup = BeautifulSoup(r.content, 'html.parser')
ticker_list = get_tickers(soup)

dfd = {}
for symbol in ticker_list:
	dfd[symbol] = get_intraday_data(symbol)
print dfd['PIXY']
exit()
#print dataframe_list.keys()
max_diff_total = 0
min_diff_total = 0
print 'OPEN\tMAX Diff\tMIN Diff'
for ticker in dfd.keys():
	max_times = []
	min_times = []
	df = dfd[ticker]
	dayop = df.iloc[0]['open']
	peak_values = df.loc[df['time'] == '10:15:00']
	max_values = df.loc[df['high'] == df['high'].max()]
	min_values = df.loc[df['low'] == df['low'].min()]
	for index in max_values.index.values:
		max_times.append(max_values['high'][index])
	for index in min_values.index.values:
		min_times.append(min_values['high'][index])
	#print '{0}\t{1}\t{2}'.format(dayop,max_times,min_times)
	max_diff = max_times[0] - dayop
	min_diff = dayop - min_times[0]
	print '{0}\t{1}\t{2}'.format(ticker,max_diff,min_diff)
	max_diff_total = max_diff_total + max_diff
	min_diff_total = min_diff_total + min_diff
print 'Total\t{0}\t{1}'.format(max_diff_total,min_diff_total)
#max_times_unique = list(set(max_times))
#min_times_unique = list(set(min_times))
#print 'max times'
#for i in max_times_unique:
#	print '{0}\t{1}'.format(i,max_times.count(i))
#print 'min times'
#for i in min_times_unique:
	#print '{0}\t{1}'.format(i,min_times.count(i))
	#max_times.append(max_values['time'][index] for index in max_values.index.values)
	#value_list.append({'ticker':ticker,'open':open_values['open'],'max':[max_values['high'],max_values['time']]})
	#print '{0}\nopen:{1}\nmax:{2}\t{3}\n\n'.format(ticker,dayop,list(max_values['high'][index] for index in max_values.index.values),list(max_values['time'][index] for index in max_values.index.values))
	#	