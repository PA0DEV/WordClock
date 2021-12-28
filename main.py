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
#   2 -> builtin LED
#   5 -> I2C clock
#   4 -> I2C data
# 
# used external libaries:
#  - ds3231.py
# ----------------------------------------
### imports ###
import network
from machine import Pin, SoftI2C
import ds3231
import ntptime
from time import sleep, localtime

# ----------------------------------------
timezone = 1
wDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)
rtc = ds3231.DS3231(i2c)




while True:
    time = rtc.get_time()       # (year, month, day, hour, minute, second, wday, 0)
    year = time[0]
    month = time[1]
    day = time[2]
    hour = time[3] + timezone
    minute = time[4]
    second = time[5]
    wday = wDays[time[6]]

    print("Current time: %s, %i.%i.%i ; %i:%i:%i"%(wday, day, month, year, hour, minute, second,))
    
    sleep(1)
