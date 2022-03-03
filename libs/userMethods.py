


import time
import datetime


def summertimeStart(year):
    for i in range(6):
        date = datetime.date(year, 3, 31-i)
        if date.weekday() == 6:
            break
    print("Summertime start: " + str(date))
    return date

def summertimeEnd(year):
    for i in range(6):
        date = datetime.date(year, 10, 31-i)
        if date.weekday() == 6:
            break
    print("Summertime end: " + str(date))
    return date

def checkSummertime(tse):
    tm = time.gmtime(tse) 
    stStart = summertimeStart(tm.tm_year)
    stEnd = summertimeEnd(tm.tm_year)
    now = datetime.datetime.fromtimestamp(tse)
    stStartUTC = datetime.datetime.combine(stStart, datetime.time(2))
    print(stStartUTC)
    print(now)
    stEndUTC = datetime.datetime.combine(stEnd, datetime.time(3))
    if stEndUTC > now > stStartUTC:
        print("Summer")
    else:
        print("Winter")
    ...

checkSummertime(datetime.datetime(2022, 3, 27, 1).timestamp())
