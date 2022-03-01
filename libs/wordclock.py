from machine import Pin
import neopixel
import json
from time import sleep

class WordClock:
    # LED addres definition
    clockWords = {
        "ES_IST": [0, 1, 2, 3, 4],
        "minutes":{
            [], # 0                                                                # 00
            [5, 6, 7, 8, 30, 31, 32, 33],                                          # 05
            [19, 20, 21, 22, 30, 31, 32, 33],                                      # 10
            [5, 6, 7, 8, 19, 20, 21, 22, 30, 31, 32, 33],                          # 15
            [9, 10, 11, 12, 13, 14, 15, 30, 31, 32, 33],                           # 20
            [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 30, 31, 32, 33],   # 25
            [35, 36, 37, 38],                                                      # 30
            [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 38, 39, 40],       # 35
            [9, 10, 11, 12, 13, 14, 15,38, 39, 40],                                # 40
            [5, 6, 7, 8, 19, 20, 21, 22, 38, 39, 40],                              # 45
            [19, 20, 21, 22, 38, 39, 40],                                          # 50
            [5, 6, 7, 8, 38, 39, 40],                                              # 55
        },
        "hours": {
            [83, 84, 85, 86, 87],       # 00
            [56, 57, 58, 59],           # 01
            [49, 50, 51, 52],           # 02 
            [60, 61, 62, 63],           # 03
            [64, 65, 66, 67],           # 04
            [45, 46, 47, 48],           # 05
            [72, 73, 74, 75, 76],       # 06
            [77, 78, 79, 80, 81, 82],   # 07
            [68, 69, 70, 71]            # 08
            [41, 42, 43, 44]            # 09
            [95, 96, 97, 98]            # 10
            [53, 54, 55],               # 11
            [83, 84, 85, 86, 87]        # 12
        },
        "MORGENS": [88, 89, 90, 91, 92, 93, 94],   # AM
        "ABENDS": [99, 100, 101, 102, 103, 104]   # PM
    }
    DEFALUT_COLOR = (0, 0, 100)
    LED_CNT = 104

    prefixColor = DEFALUT_COLOR
    minuteColor = DEFALUT_COLOR
    hourColor = DEFALUT_COLOR
    postfixColor = DEFALUT_COLOR


    def __init__(self, ledPin):
        """
        Word Clock to display the time in Words (5-Minute-Steps)
        Default color: blue (0, 0, 100)
        
            :param ledPin: Pis the LEDs are connected to
            :return: returns nothing
        """
        global np
        # initiate NeoPixel
        np = neopixel.NeoPixel(Pin(ledPin), self.LED_CNT)
        for addr in range(self.LED_CNT):
            np[addr] = (0, 0, 0)
        np.write()

        ...

    def updateColor(self, prefix, minute, hour, daytime):
        """
        Update wordclock colors

            :param prefix: color "ES IST" (R, G, B)
            :param minute: color minutes (R, G, B)
            :param hour: color hours (R, G, B)
            :param daytime: color "MORGENS" / "ABENDS" (R, G, B)
            :return: returns nothing 
        """
        self.prefixColor = prefix
        self.minuteColor = minute
        self.hourColor = hour
        self.postfixColor = daytime
        ...

    def updateTime(self, hour, minute):
        """
        update the wordclock time

            :param hour: Time hour (int)
            :param minute: Time minutes (int)
            :return: returns nothing
        """
        global np
        # turn all leds off
        for addr in range(self.LED_CNT):
            np[addr] = (0, 0, 0)
        
        # update "ES IST"
        for addr in self.clockWords["ES_IST"]:
            np[addr] = self.prefixColor

        # update minutes
        for addr in self.clockWords["minutes"][minute // 5]:
            np[addr] = self.minuteColor

        # update hours
        for addr in self.clockWords["hours"][hour]:
            np[addr] = self.hourColor

        # update "MORGENS" / "ABENDS"
        if hour < 12:
            for addr in self.clockWords["MORGENS"]:
                np[addr] = self.postfixColor
        elif hour >=12 :
            for addr in self.clockWords["ABENDS"]:
                np[addr] = self.postfixColor
        
        np.write()

    def testLEDs(self, delay, color):
        """
        Method to test the LEDs

            :param delay: the delay in between the steps
            :param color: the color to test the LEDs
            :return: returns nothing
        """
        for addr in range(self.LED_CNT):
            np[addr] = (0, 0, 0)
        np.write()

        for addr in range(self.LED_CNT):
            for i in range(self.LED_CNT):
                np[i] = (0, 0, 0)
            np[addr] = color
            np.write()
            sleep(delay)
            
        