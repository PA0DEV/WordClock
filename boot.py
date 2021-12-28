#
# name: Phillip Ahlers 
# created:  24.12.2021
# class: ETS2021
#
#
# use:
#  - connect to wifi AP and test the connection
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

import network
import json
import time


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