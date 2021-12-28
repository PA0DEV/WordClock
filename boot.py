#
# name: Phillip Ahlers 
# created:  24.12.2021
# class: ETS2021
#
#
# use:
#  - connect to wifi AP and test the connection
#  - check newest firmware online
# 
# version: 0.0.1
# designed and tested on Wemos D1 mini (ESP8266)
#
# pin conenctions:
# 
# 
# used external libaries:
# 
# ----------------------------------------
### imports ###

from typing import DefaultDict
import network
import json
import time
import requests

# ----------------------------------------
## collect  WIFI setup data ##
with open("settings.json") as f:
    settings = json.load(f)

wifiSSID = settings["wifi"]["ssid"]
wifiPass = settings["wifi"]["pass"]
wifiDHCP = settings["wifi"]["dhcp"]
wifiClientIP = settings["wifi"]["client"]
wifiSubnet = settings["wifi"]["subnet"]
wifiGateway = settings["wifi"]["gateway"]

# ----------------------------------------
## collect info data ##
with open("info.json") as f:
    info = json.load(f)

# ----------------------------------------
## Network setup ##
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

    ## dynamic ip or static ip ##
if wifiDHCP:
    if not wifi.isconnected():
        wifi.connect(wifiSSID, wifiPass)
else:
    wifi.ifconfig((wifiClientIP, wifiSubnet, wifiGateway, '8.8.8.8'))
    if not wifi.isconnected():
        wifi.connect(wifiSSID, wifiPass)

## start try to connect to ap ##
start = time.time()
while not wifi.isconnected() and time.time() - start < 15:
    ## connection timeout after 15s ##
    pass

## check if connected ##
if wifi.isconnected():
    ## device is online ##
    info["device"]["online"] = True
    info["device"]["clientIP"] = wifi.ifconfig()[0]
    ...

else:
    ## error code here ##
    info["device"]["online"] = False
    ...
with open("info.json", "w") as f:
    json.dump(info, f)

# ----------------------------------------
## Version check ##
autoUpdate = settings["updates"]["autoUpdate"]
updateOnBoot = settings["updates"]["updateOnBoot"]
    ## check own version ##


    ## get newest version online ##
if autoUpdate or updateOnBoot:
    ownVersion = info["general"]["version"]
    fwUrl = settings["updates"]["updateURL"]
    remoteVersion = requests.get(fwUrl + "info.json").text
    remoteVersion = json.loads(remoteVersion)
    remoteVersion = remoteVersion["general"]["version"]

    if remoteVersion > ownVersion:
        ### Update code###
        ...
        res = requests.get(fwUrl + "files.json").text
        files = json.loads(res)

        with open("files.json", "w") as f:
            json.dump(files, f)

        for file in files:
            with open(file, "w") as f:
                

    else:
        ### no update ###
        pass


    