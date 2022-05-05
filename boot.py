# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Phillip Ahlers                                          #
# ETS2021                                                 #
# Platinenprojekt                                         #
# Wortuhr                                                 #
# File: setup.py
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Imports # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from libs import wifiManager, autoUpdater
import machine

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Global Setup Variables  # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
REPO_URL = "https://github.com/PA0DEV/WordClock"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Start WiFi Manager  # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# start the wifi Manager and get the active connection 
WiFi = wifiManager.getConnection()

if WiFi is None:
    # cannot connect to any network
    print("[WifiMgr] Could not initialize the network connection.")

    while True:
        # you shall not pass
        pass
else:
    # wifi is connected
    print("[WifiMgr] ESP OK")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Automatic Firmware Updater  # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

updater = autoUpdater.Updater(REPO_URL)
reqReboot = updater.downloadUpdate()

if reqReboot:
    # hard reset the board
    machine.reset()
else:
    # continue to main.py
    pass