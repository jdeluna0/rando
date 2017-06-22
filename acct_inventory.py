import requests
import getpass
import json
from pathlib import Path
import warnings
from collections import defaultdict
import sys

SSO = 'jame9129'
ACCT = '34231' # Walmart Inkiru
#ACCT = '3022692' # Walmart Store Returns
#ACCT = '970854' # Walmart CAP
#ACCT = '858926' # EA
#ACCT = '814851' # Glassdoor
#ACCT = '815298' # Hilton Grand Vacations

def get_token():
    ### Commented section saves the token so you don't have to keep entering your RSA. Not secure but convenient... ###
#    token_file = Path("/Users/jame9129/.tokens/coretoken.txt")
#    if token_file.is_file():
#        with file("/Users/jame9129/.tokens/coretoken.txt") as f:
#            test_token = f.read()
#        req = requests.get("https://ws.core.rackspace.com/ctkapi/session/{0}".format(test_token))
#        validate_token = json.loads(req.content)
#        if validate_token["valid"] == True:
#            token = test_token
#            return token
    rsa = getpass.getpass("PIN + RSA: ")
    header = {'Content-Type': 'application/json'}
    payload = {'password': rsa}
    url = "https://ws.core.rackspace.com/ctkapi/login/{0}".format(SSO)
    req = requests.post(url, json=payload, headers=header)
    token = json.loads(req.content)["authtoken"]
#    f = open( '/Users/jame9129/.tokens/coretoken.txt', 'w' )
#    f.write(token)
    return token

def logout():
    url = "https://ws.core.rackspace.com/ctkapi/logout/{0}".format(token)
    req = requests.get(url)
    print req
    print req.text

def device_count(dc, groups_dict):
    print dc
    total = 0
    for keys in groups_dict.keys():
        print '\t',"{0:<70}{1:>9}".format(keys,len(groups_dict[keys]))
    return

def platforms(token, option=''):
    header = {'Content-Type': 'application/json', 'X-Auth': token}
    url = "https://ws.core.rackspace.com/ctkapi/query/"
    
    offset = 0
    devices_dict = {}
    while offset != -1:

        payload = [
                    {
                 "class": "Computer.Computer",
                        "load_arg": {
                                "class": "Computer.ComputerWhere",
                                        "values": [
                                                ["account", "=",  ACCT],
                                                "&",
                                                ["status","<>",'-1']
                                        ],
                                        "limit": 250,
                                        "offset": offset
                                },
                        "load_method": "loadList",
                        "attributes": [
                                "number",
                                "name",
                                "datacenter.symbol",
                                "status.name",
                                "account.number",
                                "account.name",
                                "platform_model"]
                }
            ]
        req = requests.post(url, json=payload, headers=header)
        response = json.loads(req.content)

        if req.status_code != 200:
            print response["error_message"]
            exit()

        for device_stats in response: #format of response are dicts within a dict within a list
            if not device_stats['result']: #checks if device list is empty
                offset = -1
                break
            offset = offset + 250
            for computers in device_stats['result']:
                if computers['datacenter.symbol'] not in devices_dict:
                    devices_dict[computers['datacenter.symbol']] = [(computers['platform_model'],computers['name'])]
                else:
                    devices_dict[computers['datacenter.symbol']].append((computers['platform_model'],computers['name']))
    
    ### Out of while loop
    if option == '--count' or option == '-c':
        for datacenter in devices_dict.keys():
            groups_dict = defaultdict(list)
            for platform,name in devices_dict[datacenter]:
                groups_dict[platform].append(name)
            device_count(datacenter, groups_dict)
        return

    for datacenter in devices_dict.keys():
        groups_dict = defaultdict(list)
        for platform,name in devices_dict[datacenter]:
            groups_dict[platform].append(name)

        print datacenter
        for keys in groups_dict.keys():
            print
            print '\t',keys
            print
            for item in groups_dict[keys]:
                print '\t\t',item
    return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        option = sys.argv[1]
    if option == '-h' or option == '--help':
        print 'Usage: {0} [options]\n\nRunning the script without arguments will return a list of hostnames for each platform\n\nOptions:\n\t-c\tLists a count of account devices per platform organized by datacenter\n\t-l\tInvalidates token on local machine\n'.format(sys.argv[0])
        exit()

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        
       
        token = get_token()
        if option == '-l' or option == '--logout':
            logout(token)
            exit()

        platforms(token, option)
