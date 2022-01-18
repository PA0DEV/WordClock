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
#   14 -> Data LED Words
#   12 -> Data LED Segments
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
iyear = 0
imonth = 1
iday = 2
ihour = 3
iminute = 4
isecond = 5
iweekday = 6
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
if info["device"]["online"] == True and settings["clock"]["autoTimeset"] == True:
    server = settings["clock"]["timeserver"]
    ntptime.settime(server)                 # get time from server
    rtc.save_time()                         # set RTC mudule time

# ----------------------------------------
### LED addresses ###
# Segments
#      __ __ __        __ __ __          __ __ __        12 13 14  
#    __        __    __        __      __        __    11        15
#    __        __    __        __      __        __    10        16
#    __        __    __        __  42  __        __    _9        17
#      __ __ __        __ __ __          __ __ __        20 19 18  
#    __        65    __        44  43  __        21    _8        _0
#    __        __    __        __      __        __    _7        _1
#    __        __    __        __      __        __    _6        _2
#       __ __ __       __ __ __           __ __ __       _5 _4 _3   

## offset address for first segment LED
segOffset = [105, 126, 149, 170]

## address dot LEDs
segDots = [147, 148]

# address segment number / symbol
segNumbers = [
    [0, 1, 2, 3, 4, 5, 67, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],               # 0
    [0, 1, 2, 15, 16, 17],                                                      # 1
    [3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20],                     # 2
    [0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20],                     # 3
    [0, 1, 2, 9, 10, 11, 15, 16, 17, 18, 19, 20],                               # 4
    [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 18, 19, 20],                      # 5
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 20],             # 6
    [0, 1, 2, 12, 13, 14, 15, 16, 17],                                          # 7
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], # 8
    [0, 1, 2, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],                   # 9
    [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],                            # °
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],                                  # C
    [3, 7 , 8, 9, 10, 11, 12, 13, 14, 18, 19, 20],                              # F
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 20],                      # E
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 17],                         # U
    [6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 20],                               # P
    [18, 19, 20]                                                                # -
]
## LED address prefix ##
dispItIs = [0, 1, 2, 3, 4]

## LED address hours ##
dispHours = [
    [83, 84, 85, 86, 87],       # 00 | 12
    [56, 57, 58, 59],           # 01
    [49, 50, 51, 52],           # 02 
    [60, 61, 62, 63],           # 03
    [64, 65, 66, 67],           # 04
    [45, 46, 47, 48],           # 05
    [72, 73, 74, 75, 76],       # 06
    [77, 78, 79, 80, 81, 82],   # 07
    [68, 69, 70, 71]            # 08
    [41, 42, 43, 44]            # 09
    [95, 96, 97, 98]            # 10
    [53, 54, 55]                # 11
]

## LED address minutes ##
dispMins = [
    [], # 0                                                                # 00
    [5, 6, 7, 8, 30, 31, 32, 33],                                          # 05
    [19, 20, 21, 22, 30, 31, 32, 33],                                      # 10
    [5, 6, 7, 8, 19, 20, 21, 22, 30, 31, 32, 33],                          # 15
    [9, 10, 11, 12, 13, 14, 15, 30, 31, 32, 33],                           # 20
    [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 30, 31, 32, 33],   # 25
    [35, 36, 37, 38],                                                      # 30
    [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 38, 39, 40],       # 35
    [9, 10, 11, 12, 13, 14, 15,38, 39, 40],                                # 40
    [5, 6, 7, 8, 19, 20, 21, 22, 38, 39, 40],                              # 45
    [19, 20, 21, 22, 38, 39, 40],                                          # 50
    [5, 6, 7, 8, 38, 39, 40],                                              # 55
]

## LED address morning / afternoon ##
dispAmPm = [
    [88, 89, 90, 91, 92, 93, 94],   # AM
    [99, 100, 101, 102, 103, 104]   # PM
]

# ----------------------------------------
### setup async time and temperature update ###
async def getTimeAndTemp():
    global utcTime
    global locTime
    global temp
    while True:
        

        timezone = settings["clock"]["timezone"]
        

        utcTime = rtc.get_time()       # returns [year, month, day, hour, minute, second, wday, 0] (UTC time)

        dstHour = utcTime[ihour] + timezone

        year = utcTime[iyear]
        month = utcTime[imonth]
        day = utcTime[iday]
        ## check for summer- wintertime
        if 4 < month < 9 or (month == 3 and (day > 27 or day == 27 and dstHour > 2) ) or (month == 10 and (day <30 or day == 30 and dstHour < 3)) :
            ## summertime from mar 27 2:00 to oct 30 3:00
            hour = utcTime[ihour] + timezone +1
        else :
             hour = utcTime[ihour] + timezone
        
        minute = utcTime[iminute]
        second = utcTime[isecond]
        wDay = utcTime[iweekday]

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
### write wordclock ###
async def displayWords():
    ### Words LED controll ### 
    for adr in dispItIs:
        print(adr)
        ## LED CODE ##
        ...
    for adr in dispHours[locTime[ihour]]:
        print(adr)
        ## LED CODE ##
        ...
    for adr in dispMins[locTime[iminute] // 5]:
        print(adr)
        ## LED Code ##
        ...
    for adr in dispHours[locTime[ihour] // 12]:
        print(adr)
        ## LED Code ##
        ...

    await uasyncio.sleep_ms(1000)

# ----------------------------------------
### write clock on segments ###
async def segmentClock():
    ## Segment 0 - 1 minute ##
    number = locTime[iminute] % 10
    for adr in segNumbers[number]:
        adr += segOffset[0]
        ...
    
    ## Segment 1 - 10 minute ##
    number = locTime[iminute] // 10
    for adr in segNumbers[number]:
        adr += segOffset[1]
        ...

    ## Segment 2 - 1 hour ##
    number = locTime[ihour] % 10
    for adr in segNumbers[number]:
        adr += segOffset[2]
        ...

    ## Segment 3 - 10 hour
    number = locTime[ihour] // 10
    for adr in segNumbers[number]:
        adr += segOffset[3]
        ...
    
    ## dots ##
    for adr in segDots:
        ...
    uasyncio.sleep(1000)
    for adr in segDots:
        ...

# ----------------------------------------
### start the methods ###
async def run():
    while True:
        task1 = uasyncio.create_task(getTimeAndTemp())
        task2 = uasyncio.create_task(display())
        

        await task1
uasyncio.run(run())