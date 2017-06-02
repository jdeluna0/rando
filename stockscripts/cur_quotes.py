#!/usr/bin/env python

from googlefinance import getQuotes
import json


print json.dumps(getQuotes(['NEO', 'SLW']), indent=2)
