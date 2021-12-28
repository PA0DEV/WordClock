#
# name: Phillip Ahlers 
# created:  24.12.2021
#
#
# use:
#  - connect to wifi AP and test the connection
#  - check newest firmware online
#  - download and update code from https://github.com/PA0DEV/WordClock
# 
# version: 0.0.0
# designed and tested on Wemos D1 mini (ESP8266)
#
# pin conenctions:
# 
# 
# used external libaries:
# 
# ----------------------------------------
### imports ###
print()
print()
print()

import network
import machine
import json
import time
import urequests

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
        print("[WIFI] Trying to connect to ap: %s ; %s" %(wifiSSID, wifiPass))
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
    print("[WIFI] Connected! IP: %s"%(wifi.ifconfig()[0]))
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
    print("[Update] Own version: %s"%(ownVersion))
    fwUrl = settings["updates"]["updateURL"]
    remoteVersion = urequests.get(fwUrl + "info.json").text
    remoteVersion = json.loads(remoteVersion)
    remoteVersion = remoteVersion["general"]["version"]
    print("[Update] Remote version: %s"%(remoteVersion))
    if remoteVersion > ownVersion:
        ### Update code###
        print("[Update] Starting update...")
        ...
        res = urequests.get(fwUrl + "files.json").text
        files = json.loads(res)

        with open("files.json", "w") as f:
            json.dump(files, f)

        for file in files:
            print(files[file])

            with open(files[file], "w") as f:
                payload = urequests.get(fwUrl + files[file]).text
                f.write(payload)
        print("[Update] Update successfull!")
        print("[Update] Rebooting...")
        machine.reset()
    else:
        ### no update ###
        print("[Update] no update found...")
        pass


    