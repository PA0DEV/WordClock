import json
from turtle import width
try:
    import requests
except:
    import urequests as requests


class Updater:
    def __init__(self, repoUrl):
        """
        Update Micropython code from public github repository

            :param repoUrl: URL of the repository
            :return: returns nothing 
        """
        self.repoUrl = repoUrl
        
        ...

    def checkVersion(self):
        """
        Check and comare the current version of the Software to the version available
        
            :return: returns true if there is a new version available
        """

        # check for available internet connection
        if not self.isOnline():
            return False
        
        # read own fw version
        with open("./settings/info.json") as f:
            ownFw = json.load(f)["device"]["version"]
            print(ownFw)

    def downloadUpdate(self):
        ...

    def isOnline(self):
        """
        Check if the controller is connected to the Internet
        
            :return: retunrs nothing
        """
        # check for available internet connection
        try:
            request = requests.get("http://www.google.com", timeout=5)
            return True
        except:
            return False

######################################
# create file / folder file
#!!!! needs to be run before publish !!!!
if __name__ == "__main__":
    from os.path import isfile, join
    from os import listdir

    try:
        mainfiles = [f for f in listdir("./") if isfile(join("./", f))]
    except:
        mainfiles = []
    try:
        libFiles = [f for f in listdir("./libs") if isfile(join("./libs", f))]
    except:
        libFiles = []
    try:
        settingFiles = [f for f in listdir("./settings") if isfile(join("./settings", f))]
    except:
        settingFiles = []

    files = {
        "libs": libFiles,
        "main": mainfiles,
        "settings": settingFiles
    }
    
    with open("./settings/files.json", "w") as f:
        f.write(json.dumps(files))

    print(files)
else:
   pass