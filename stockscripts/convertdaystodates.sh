#!/bin/bash

if [ "$#" = 0 ];then
	echo "USAGE: convertdaytodates.sh <number of days back> <day of the week, first 3 letters> <name of file to save>"
	exit 0
fi

numdayz=$1
wday=$2
filename=$3

for i in `seq 0 $numdayz`; do date -d "-$i day" ;done | grep $wday | sed 's/\s\s*/ /g' | cut -d " " -f2,3,6 > $filename

sleep 5

date +"%Y-%m-%d" -f $filename > $filename_con.txt
