
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Imports # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
try:
    import asyncio
except:
    import uasyncio as asyncio

from libs import segments
from libs import timeSync

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Pin definitions # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
RTC_SDA_PIN = 0
RTC_SCL_PIN = 0
LED_PIN = 0 
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
        asyncio.sleep_ms(500)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Initiate Segments # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

SEGMENTS_MODE = 0 # 0 = Clock, 1 = Date, 2 = Temperature, 3 = Cycle

segment = segments.Segments(LED_PIN)


async def segmentUpdate():
    if SEGMENTS_MODE == 0:
        # Clock Mode
        global actTime
        segment.setDoubleSegment(0, actTime[5]) # Display minutes
        segment.setDoubleSegment(2, actTime[4]) # Display seconds
        asyncio.sleep_ms(1000)

    elif SEGMENTS_MODE == 1:
        # Date Mode
        pass

    elif SEGMENTS_MODE == 2:
        # Temperature mode
        pass
    
async def segmentDots():
    if SEGMENTS_MODE == 0:
        # Clock mode --> Blink with 1 Hz
        segment.setDots(True)
        asyncio.sleep_ms(500)
        segment.setDots(False)
        asyncio.sleep_ms(500)

    elif SEGMENTS_MODE == 1:
        # Date Mode --> No dots
        segment.setDots(False)
        asyncio.sleep_ms(500)
        pass

    elif SEGMENTS_MODE == 2:
        # Temperature mode --> no Dots
        segment.setDots(False)
        asyncio.sleep_ms(500)
        pass


async def main():
    t1 = asyncio.create_task(segmentUpdate)
    t2 = asyncio.create_task(segmentDots)
    t3 = asyncio.create_task(updateTime)
    await t1, t2

asyncio.run(main())