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
from machine import Pin, SoftI2C
import ds3231
import ntptime
import dht
from time import sleep, localtime

# ----------------------------------------
### setup rtc module ###
timezone = 1
wDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)
rtc = ds3231.DS3231(i2c)

# ----------------------------------------
### setup DHT11 module ###
sensor = dht.DHT11(Pin(0))



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
    sensor.measure()
    temp = sensor.temperature()
    humid = sensor.humidity()

    print("Temperature: %2.1f"%temp)
    print("Humidity: %2.1f"%humid)
    print()
    
    sleep(1)
