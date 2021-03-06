import RPi.GPIO as GPIO
import time

def control():
    GPIO.setmode(GPIO.BCM)
    door = 23

    GPIO.setup(door, GPIO.OUT, initial=GPIO.LOW)

    GPIO.output(door, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(door, GPIO.LOW)
    time.sleep(0.5)

    GPIO.cleanup()
