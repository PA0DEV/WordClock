#
# name: Phillip Ahlers 
# created:  24.12.2021
#
#
# use:
#
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
try:
    import gc
    gc.collect()
except:
    pass

from libs import webserver
try:
    import uasyncio as asyncio
except:
    import asyncio

ssid = 'BZTG-IoT'
password = 'WerderBremen24'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


webSrv = webserver.WebServer()



async def webHandler():
    while True:
        webSrv.listenClient()
        await asyncio.sleep(0.1)

async def main():
    t1 = asyncio.create_task(webHandler())

    await t1

asyncio.run(main())