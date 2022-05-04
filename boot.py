# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Phillip Ahlers                                          #
# ETS2021                                                 #
# Platinenprojekt                                         #
# Wortuhr                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Imports # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from libs import wifiManager, autoUpdater
import machine

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Global Setup Variables  # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
REPO_URL = ""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Start WiFi Manager  # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

WiFi = wifiManager.getConnection()

if WiFi is None:
    # cannot connect to any network
    print("[WifiMgr] Could not initialize the network connection.")

    while True:
        # you shall not pass
        pass
else:
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