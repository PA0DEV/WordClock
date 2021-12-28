import json
from os import write
import requests

fwUrl = "https://raw.githubusercontent.com/PA0DEV/WordClock/main/"

ownVersion = "0.0.0"
remoteVersion = requests.get(fwUrl + "info.json").text
remoteVersion = json.loads(remoteVersion)
remoteVersion = remoteVersion["general"]["version"]

print(remoteVersion)

if remoteVersion > ownVersion:
    ### Update code###
    res = requests.get(fwUrl + "files.json").text
    files = json.loads(res)

    with open("files.json", "w") as f:
        json.dump(files, f)

    for file in files:
        print(files[file])

        with open("test_" + files[file], "w") as f:
            payload = requests.get(fwUrl + files[file]).text
            f.write(payload)

