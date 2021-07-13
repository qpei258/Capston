from Adafruit_AMG88xx import Adafruit_AMG88xx
from time import sleep

def tempcheck():
    sensor = Adafruit_AMG88xx()
    sleep(.1)

    max = 0

    for i in sensor.readPixels():
        if i > max:
            max = i
    return max