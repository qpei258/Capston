#!/usr/bin/python
from Adafruit_AMG88xx import Adafruit_AMG88xx
from time import sleep
sensor = Adafruit_AMG88xx()

def tempcheck():
    sleep(.1)

    max = 0
    for i in sensor.readPixels():
        if i > max:
            max = i
    return max
