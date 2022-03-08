import time
from libs import ds3231
from machine import SoftI2C, Pin, RTC

# (year, month, mday, hour, minute, second, weekday, yearday)

class TimeSync:
    def __init__(self, rtcSDA, rtcSCL) -> None:
        """
        Initiate the Time Sync
        
            :param rtcSDA: rtc module Serial Data Pin
            :param enDST: rtc module Serial Clock Pin
            :return: returns nothing
        """
        from libs import ds3231
        i2c = SoftI2C(scl=Pin(rtcSCL), sda=Pin(rtcSDA), freq=100000)
        self.rtc = ds3231.DS3231(i2c)        

    
    def syncTime(self):
        """
        Sync the time with NTP-Server
        
            :return: returns nothing
        """
        import ntptime
        ntptime.settime()


    def cettime(self):
        """
        convert the current UTC-Time to CET / CEST
        (year, month, mday, hour, minute, second, weekday, yearday)
        
            :return: returns the current Central Europe time
        """

        year = time.localtime()[0]       #get current year
        HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to CEST
        HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
        now=time.time()
        if now < HHMarch :               # we are before last sunday of march
            cet=time.localtime(now+3600) # CET:  UTC+1H
        elif now < HHOctober :           # we are before last sunday of october
            cet=time.localtime(now+7200) # CEST: UTC+2H
        else:                            # we are after last sunday of october
            cet=time.localtime(now+3600) # CET:  UTC+1H
        return(cet)

    def saveTimeToRtc(self):
        """
        Save the current time to the RTC Module
            :return: returns nothing"""

        self.rtc.save_time()
    
    def getTimeFromRtc(self):
        """
        Get the current time from the RTC module
            :return: returns nothing
        """
        tm = self.rtc.get_time(set_rtc=True)
        RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))