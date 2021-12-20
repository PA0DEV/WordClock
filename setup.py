import json
from os import write
import requests

## load own version info from json ##
with open('version.json') as f:
    info = json.load(f)
ownVersion = info["version"]

## load newest version from github ##
r = requests.get("https://raw.githubusercontent.com/PA0DEV/WordClock/main/version.json")

    # Status code 200 = OK
if r.status_code == 200:
    newestInfo = json.loads(r.text)
    newestVersion = newestInfo["version"]
else:
    ###---Error Code ---###
    ...

if newestVersion > ownVersion:
    ###---Update Code---###
    with open('NEWmain.py', 'w') as f:
        write(requests.get("https://raw.githubusercontent.com/PA0DEV/WordClock/main/main.py").text)
    ...
    
    
elif newestVersion == ownVersion:
    ###---Normal Code---###
    ...
    