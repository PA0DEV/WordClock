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
    print(newestVersion)
else:
    ###---Error Code ---###
    ...

if newestVersion > ownVersion:
    ###---Update Code---###
    f = open("NEWmain.py", "a")
    r = requests.get("https://raw.githubusercontent.com/PA0DEV/WordClock/main/main.py").text
    print(r)
    f.write(r)
    f.close()
    ...
    
    
elif newestVersion == ownVersion:
    ###---Normal Code---###
    ...
    