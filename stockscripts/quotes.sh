#!/bin/bash

# $1 is NEO
# $3 is SLW
# grabs the price of each stock
NEO=`python ~/scripts/cur_quotes.py | grep -i "price\|symbol" | cut -d : -f 2 | sed -e 's/"//g' -e 's/,//g' | awk 'BEGIN {RS = "" ; FS = "\n"}; { print $1}' | bc`
SLW=`python ~/scripts/cur_quotes.py | grep -i "price\|symbol" | cut -d : -f 2 | sed -e 's/"//g' -e 's/,//g' | awk 'BEGIN {RS = "" ; FS = "\n"}; { print $3}' | bc`

if [ 1 -eq "$(echo "$NEO < 8.7" | bc)" ]; then
	echo "NEO is below 8.70" | mutt -s "Stock things" 2107604057@msg.fi.google.com	
fi

if [ 1 -eq "$(echo "$SLW > 18" | bc)" ]; then
	echo "SLW is above 18" | mutt -s "Stock things" 2107604057@msg.fi.google.com	
	else
		echo "SLW is below 22." >> /root/logs/slw.log
fi
if [ 1 -eq "$(echo "$SLW < 17" | bc)" ]; then
	echo "SLW is below 17" | mutt -s "Stock things" 2107604057@msg.fi.google.com	
fi

