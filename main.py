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
wDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)
rtc = ds3231.DS3231(i2c)
espTime = RTC()
espTime = rtc.get_time()
# ----------------------------------------
### setup DHT11 module ###
sensor = dht.DHT11(Pin(0))

# ----------------------------------------
### collect settings data ###
with open("settings.json") as f:
    settings = json.load(f)
# ----------------------------------------
### setup async time and temperature update ###
async def getTimeAndTemp():
    while True:
        global time
        global temp

        timezone = settings["clock"]["timezone"]
        

        time = rtc.get_time()       # returns [year, month, day, hour, minute, second, wday, 0] (UTC time)
        
        year = time[0]
        month = time[1]
        day = time[2]
        if 
        hour = time[3] + timezone
        minute = time[4]
        second = time[5]
        wday = wDays[time[6]]

        print("Current time: %s, %i.%i.%i ; %i:%i:%i"%(wday, day, month, year, hour, minute, second,))

        

        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()

        print("Temperature: %2.1f"%temp)
        print("Humidity: %2.1f"%humid)
        print()
        
        await uasyncio.sleep_ms(1000)

# ----------------------------------------
### start the methods ###
async def run():
    while True:
        task1 = uasyncio.create_task(getTimeAndTemp())
        

        await task1
uasyncio.run(run())