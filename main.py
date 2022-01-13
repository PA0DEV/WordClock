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
# external hardware: 
#  - RTC module (DS3231)
#  - Temperature and humidity sensor (DHT11)
#
# pin conenctions:
#   2 -> builtin LED
#   5 -> I2C clock
#   4 -> I2C data
#   0 -> DHT data
# 
# used external libaries:
#  - ds3231.py
# ----------------------------------------
### imports ###
from machine import Pin, SoftI2C, RTC
import ds3231
import ntptime
import dht
import uasyncio
import json

# ----------------------------------------
### setup rtc module ###


i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)
rtc = ds3231.DS3231(i2c)
espTime = RTC()
espTime = rtc.get_time()
# ----------------------------------------
### setup DHT11 module ###
sensor = dht.DHT11(Pin(0))

# ----------------------------------------
## collect settings / info data ###
with open("settings.json") as f:
    settings = json.load(f)

## collect info data ##
with open("info.json") as f:
    info = json.load(f)

# ----------------------------------------
### ntp sync ###
if info["device"]["online"] == True and settings["clock"]["autoTimeset"]:
    server = settings["clock"]["timeserver"]
    ntptime.settime(server)                 # get time from server
    rtc.save_time()                         # set RTC mudule time

# ----------------------------------------
### setup async time and temperature update ###
async def getTimeAndTemp():
    global utcTime
    global locTime
    global temp
    while True:
        

        timezone = settings["clock"]["timezone"]
        

        utcTime = rtc.get_time()       # returns [year, month, day, hour, minute, second, wday, 0] (UTC time)

        dstHour = utcTime[3] + timezone

        year = utcTime[0]
        month = utcTime[1]
        day = utcTime[2]
        ## check for summer- wintertime
        if 4 < month < 9 or (month == 3 and (day > 27 or day == 27 and dstHour > 2) ) or (month == 10 and (day <30 or day == 30 and dstHour < 3)) :
            ## summertime from mar 27 2:00 to oct 30 3:00
            hour = utcTime[3] + timezone +1
        else :
             hour = utcTime[3] + timezone
        
        minute = utcTime[4]
        second = utcTime[5]
        wDay = utcTime[6]

        print("Current time: %i.%i.%i ; %i:%i:%i"%(day, month, year, hour, minute, second,))

        locTime = [year, month, day, hour, minute, second, wDay]

        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()

        print("Temperature: %2.1f"%temp)
        print("Humidity: %2.1f"%humid)
        print()
        
        await uasyncio.sleep_ms(500)

# ----------------------------------------
###  ###
async def display():
    wDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dispItIs = [0, 1, 2, 3, 4]
    dispHours = [
        [83, 84, 85, 86, 87],       # 00 | 12
        [49, 50, 51, 52],           # 01
        [56, 57, 58, 59],           # 02 
        [60, 61, 62, 63],           # 03
        [64, 65, 66, 67],           # 04
        [45, 46, 47, 48],           # 05
        [68, 69, 70, 71, 72],       # 06
        [77, 78, 79, 80, 81, 82],   # 07
        [73, 74, 75, 76]            # 08
        [41, 42, 43, 44]            # 09
        [88, 89, 90, 91]            # 10
        [53, 54, 55]                # 11
    ]
    dispMins = [
        [],                                                                             # 00
        [5, 6, 7, 8, 37, 38, 39, 40],                                                   # 05
        [19, 20, 21, 22, 37, 38, 39, 40],                                               # 10
        [5, 6, 7, 8, 19, 20, 21, 22, 37, 38, 39, 40],                                   # 15
        [12, 13, 14, 15, 16, 17, 18, 19, 20, 37, 38, 39, 40],                           # 20
        [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 37, 38, 39, 40],    # 25
        [33, 34, 35, 36]                                                                # 30
        [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 31, 32],        # 35
        [12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 31, 32],                               # 40
        [5, 6, 7, 8, 19, 20, 21, 22, 30, 31, 32],                                       # 45
        [19, 20, 21, 22, 30, 31, 32],                                                   # 50
        [5, 6, 7, 8, 30, 31, 32],                                                       # 55
    ]

    while True:
        ### Words LED controll ### 
        for adr in dispItIs:
            print(adr)
            ## LED CODE ##
            ...
        for adr in dispHours[locTime[3]]:
            print(adr)
            ## LED CODE ##
            ...
        for adr in dispMins[locTime[4]]:
            print(adr)
            ## LED Code ##
            ...



# ----------------------------------------
### start the methods ###
async def run():
    while True:
        task1 = uasyncio.create_task(getTimeAndTemp())
        

        await task1
uasyncio.run(run())