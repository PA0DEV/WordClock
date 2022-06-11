import json

try:
    import requests
except:
    import urequests as requests


class Updater:
    def __init__(self, repoUrl):
        """
        Update Micropython code from public github repository

            :param repoUrl: URL of the repository ('http://www.github.com/User/Repository')
            :return: returns nothing 
        """

        # change url to raw.github.com
        index = repoUrl.find(".com")
        cutUrl = repoUrl[index+4:]
        self.repoUrl = "https://raw.githubusercontent.com" + cutUrl + "/main/"


    def isNewUpdate(self):
        """
        Check and comare the current version of the Software to the version available
        
            :return: Returns true if there is a new version available
        """

        
        
        # read own fw version
        with open("./settings/info.json") as f:
            ownFw = json.load(f)["device"]["version"]

        # get available fw version

        url = self.repoUrl + "settings/info.json"
        onlineFw = requests.get(url).text
        onlineFw = json.loads(onlineFw)
        onlineFw = onlineFw["device"]["version"]

        print("[UPDATE] Local Firmware: " + ownFw)
        print("[UPDATE] Remote Firmware: " + onlineFw)

        if onlineFw > ownFw:
            print("[UPDATE] Downloading Updates...")
            return True
        else:
            return False

    def downloadFile(self, file):
        url = self.repoUrl +  file
        print(url)
        file = requests.get(url).text
        

        return file

    def updateFile(self, file):
        with open(file, "w") as f:
            f.write(self.downloadFile(file)) 
        return


    def downloadUpdate(self):
        """
        Method to download newest update if available
        
            :return: Returns True if download is ready and need to reboot
        """
        if self.isNewUpdate():
            files = json.loads(self.downloadFile("settings/files.json"))
            print("[UPDATE] Updating")
            print()
            print("[UPDATE] Main")
            for file in files["main"]:
                if file != "README.md":         #< Ignore README.md
                    print("[UPDATE]     " + file)
                    self.updateFile(file)
                    ...
            print("libs:")
            for file in files["libs"]:
                print("[UPDATE]     " + file)
                self.updateFile("libs/" + file)
                ...
            print("settings")
            for file in files["settings"]:
                print("[UPDATE]     " + file)
                self.updateFile("settings" + file)
                ...
            

            return True
        else:
            return False


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