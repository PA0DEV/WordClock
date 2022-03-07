


import time
import datetime


def summertimeStart(year):
    for i in range(6):
        date = datetime.date(year, 3, 31-i)
        if date.weekday() == 6:
            break
    # print("Summertime start: " + str(date))
    return date

def summertimeEnd(year):
    for i in range(6):
        date = datetime.date(year, 10, 31-i)
        if date.weekday() == 6:
            break
    # print("Summertime end: " + str(date))
    return date

def checkSummertime(tse):
    """
    Checks the input time for daylight savings time

    :param tse: the time since epoch to be checked
    :return: returns true if time is dst - false if not
    """
    tm = time.gmtime(tse) 
    stStart = summertimeStart(tm.tm_year)
    stEnd = summertimeEnd(tm.tm_year)
    now = datetime.datetime.fromtimestamp(tse)
    stStartUTC = datetime.datetime.combine(stStart, datetime.time(1))
    # print(stStartUTC)
    # print(now)
    stEndUTC = datetime.datetime.combine(stEnd, datetime.time(2))
    if stEndUTC > now > stStartUTC:
        # print("Summer")
        return True
    else:
        # print("Winter")
        return False

def adjustTime(utcTime, timezone, enDst=True):
    """
    Correct UTC-Time by timezone and summer / wintertime
    
        :param utcTime: UTC Time to be corrected
        :param timezone: the current timezone (e.g. UTC+1 --> 1)
        :param enDst: enable Daylight savngs time
        :return: returns the current time as time struct
    """
    print(time.gmtime(utcTime))
    if enDst:
        if checkSummertime(utcTime):
            actTime = utcTime + (timezone + 1) * (60 * 60)
        else:
            actTime = utcTime + timezone * (60 * 60)
    else:
        actTime = utcTime + timezone * (60 * 60)
    print(time.gmtime(actTime))
    return(time.gmtime(actTime))

adjustTime(time.time(), 1)
