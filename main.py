
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Imports # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
try:
    import asyncio
    print("C")
except:
    import uasyncio as asyncio
    print("L")

from libs import segments, wordclock
from libs import timeSync
import dht
from machine import Pin, SoftI2C


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Pin definitions # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
RTC_SDA_PIN = 25
RTC_SCL_PIN = 33
LED_PIN_SEGMENT = 12
LED_PIN_WORDS = 13
DHT_PIN = 26

# print(SoftI2C(Pin(RTC_SCL_PIN),Pin(RTC_SDA_PIN)).scan())
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Initiate Temperature Sensor # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
sensor = dht.DHT11(Pin(DHT_PIN))
Temperature = 0
Humidity = 0

async def mesureTemp():
    global Temperature, Humidity
    while True:
        print("T_MES")
        sensor.measure()
        Temperature = sensor.temperature()
        Humidity = sensor.humidity()
        print(Temperature)
        await asyncio.sleep_ms(1000)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Initiate Time # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

actTime = ()
clock = timeSync.TimeSync(RTC_SDA_PIN, RTC_SCL_PIN)
try:
    clock.syncTime()
except:
    print("Could not sync Clock")
    pass



async def updateTime():
    while True:
        global actTime
        actTime = clock.cettime()   # update the local time
        await asyncio.sleep_ms(1000)
        print(actTime)
        # (year, month, mday, hour, minute, second, weekday, yearday)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Initiate Segments # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

SEGMENTS_MODE = 0 # 0 = OFF, 1 = Clock, 2 = Date, 3 = Temperature, 4 = Cycle
blinkDots = False

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


segment = segments.Segments(LED_PIN_SEGMENT)

async def displaySegment():
    while True:
        print("TIME")
        segment.setDots(True, BLUE)
        segment.setDoubleSegment(0, actTime[4], BLUE)
        segment.setDoubleSegment(2, actTime[3], BLUE)
        await asyncio.sleep_ms(5000)
        print("TEMP")
        segment.setDots(False)
        segment.setDoubleSegment(2, Temperature, GREEN)
        segment.setSegment(1, "°", GREEN)
        segment.setSegment(0, "C", GREEN)
        await asyncio.sleep_ms(5000)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Initiate Words  # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
words = wordclock.WordClock(LED_PIN_WORDS)
words.updateColor(RED, RED, RED, RED)
async def displayWords():
    words.updateTime(actTime[3], actTime[4])
    await asyncio.sleep_ms(1000)

async def main():
    t1 = asyncio.create_task(mesureTemp())
    t2 = asyncio.create_task(updateTime())
    t3 = asyncio.create_task(displaySegment())
    t4 = asyncio.create_task(displayWords())

    await t1, t2, t3, t4

asyncio.run(main())