
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Imports # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
try:
    import asyncio
except:
    import uasyncio as asyncio

from libs import segments
from libs import timeSync
import dht
from machine import Pin, SoftI2C

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Pin definitions # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
RTC_SDA_PIN = 25
RTC_SCL_PIN = 33
LED_PIN_SEGMENT = 0 
LED_PIN_WORDS = 0
DHT_PIN = 0

# print(SoftI2C(Pin(RTC_SCL_PIN),Pin(RTC_SDA_PIN)).scan())
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Initiate Temperature Sensor # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
sensor = dht.DHT11(Pin(0))
Temperature = 0
Humidity = 0

async def mesureTemp():
    while True:
        sensor.mesure()
        global Temperature, Humidity
        Temperature = sensor.temperature()
        Humidity = sensor.humidity()

        asyncio.sleep_ms(1000)


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
        asyncio.sleep_ms(100)
        print(actTime)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Initiate Segments # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

SEGMENTS_MODE = 0 # 0 = OFF, 1 = Clock, 2 = Date, 3 = Temperature, 4 = Cycle
blinkDots = False


segment = segments.Segments(LED_PIN_SEGMENT)

async def setClockMode():
    global actTime, Temperature, Humidity, blinkDots
    while True:
        if SEGMENTS_MODE == 0:
            # Turn Segments OFF
            blinkDots = False
            segment.setDots(False)
            segment.setSegment(0, None)
            segment.setSegment(1, None)
            segment.setSegment(2, None)
            segment.setSegment(3, None)
            
        elif SEGMENTS_MODE == 1:
            # Clock Mode
            blinkDots = True
            segment.setDoubleSegment(0, actTime.tm_min) # Set Minutes
            segment.setDoubleSegment(2, actTime.tm_hour) # Set Hours
            
        elif SEGMENTS_MODE == 2:
            # Date mode
            blinkDots = False
            segment.setDots(False)
            segment.setDoubleSegment(0, actTime.tm_mon) # Set Month
            segment.setDoubleSegment(2, actTime.tm_mday) # Set Day
            
        elif SEGMENTS_MODE == 3:
            # Temperature Mode
            blinkDots = False
            segment.setDots(False)
            segment.setDoubleSegment(2, int(Temperature))
            segment.setSegment(1, "°")
            segment.setSegment(0, "C")
            pass
        elif SEGMENTS_MODE == 4:
            # Cycle Mode
            pass

        asyncio.sleep_ms(20) # Update mode every 20ms

async def dots():
    global blinkDots
    while True:
        if blinkDots:
            segment.setDots(True)
            asyncio.sleep_ms(500)
            segment.setDots(False)
            asyncio.sleep_ms(500)
        else:
            segment.setDots(False)
            asyncio.sleep_ms(20)
            pass


async def main():
    # t1 = asyncio.create_task(setClockMode)
    # t2 = asyncio.create_task(mesureTemp)
    t3 = asyncio.create_task(updateTime())
    # t4 = asyncio.create_task(dots)
    # t5 = asyncio.create_task(updateTime)
    await t3

asyncio.run(main())