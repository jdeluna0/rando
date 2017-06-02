import pandas as pd
import collections

dataf = raw_input("Enter data file name: ")
print
df = pd.read_csv(dataf)
#csvobj = df.loc[df['columnl'] == value]

mmdict = {}
filename = 'friday_con.txt'
with open(filename) as dates:
	for i in dates:
		i = i.strip()
		if i not in mmdict:
			dfdate = df.loc[df['date'] == i]
			dayop = dfdate.iloc[0]["open"]
			mini = (dfdate['low'].min(),df.iloc[dfdate['low'].idxmin()]['time'])
			maxi = (dfdate['high'].max(),df.iloc[dfdate['high'].idxmax()]['time'])
			mmdict[i] = [mini,maxi,dayop]
		else:
			continue

print "DATE \t\t Min  \t\t\t Max \t\t\t Open \t\t", filename
for p in mmdict.items():
	print("{0:s} \t {1:.2f} {2:s} \t {3:.2f} {4:s} \t {5:.2f}".format(p[0],p[1][0][0],p[1][0][1],p[1][1][0],p[1][1][1],p[1][2]))
print
mmdict = {}
gaindict = {}
for i in df['date']:
	if i not in gaindict:
		gaindict[i] = 1
		daydf = df.loc[df['date'] == i]
		dayop = daydf.iloc[0]["open"]
		dayhi = float(daydf['high'].max())
		ranginc = dayhi - dayop
		gaindict[i] = ranginc

		mini = (daydf['low'].min(),df.iloc[daydf['low'].idxmin()]['time'])
                maxi = (daydf['high'].max(),df.iloc[daydf['high'].idxmax()]['time'])
                mmdict[i] = [mini,maxi,dayop]
	else:
		continue
summ = sum(gaindict.itervalues())
minn = min(gaindict.itervalues())
maxx = max(gaindict.itervalues())

print
print "Average Range/Gain from Close"
print summ / len(gaindict)
print
print "Min   Max"
print minn,maxx
print
print "DATE \t\t Min  \t\t\t Max \t\t\t Open \t\t"
orddict = collections.OrderedDict(sorted(mmdict.items()))
for p in orddict.iteritems():
        print("{0:s} \t {1:.2f} {2:s} \t {3:.2f} {4:s} \t {5:.2f}".format(p[0],p[1][0][0],p[1][0][1],p[1][1][0],p[1][1][1],p[1][2]))
