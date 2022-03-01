from libs import autoUpdater

updater = autoUpdater.Updater("https://github.com/PA0DEV/WordClock")

print(updater.downloadUpdate())