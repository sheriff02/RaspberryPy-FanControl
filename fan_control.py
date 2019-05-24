#!/usr/bin/env python3
# Author: Andreas Spiess
# Editor: Sheriff02
import os
import time
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO

sum = 0  
pTemp = 20
iTemp = 0.1

# Settings
fanPin = 18  # The pin ID, edit here to change it
desiredTemp = 54  # The maximum temperature in Celsius after which we trigger the fan
fan_speed = 100  # default value
fan_speed_min = 20
fan_speed_max = 100


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp = (res.replace("temp=", "").replace("'C\n", ""))
    # print("temp is {0}".format(temp)) #Uncomment here for testing
    return temp


def fanOFF():
    myPWM.ChangeDutyCycle(0)  # switch fan off
    return ()


def handleFan():
    global fan_speed, sum
    actualTemp = float(getCPUtemperature())
    diff = actualTemp - desiredTemp
    sum = sum + diff
    pDiff = diff * pTemp
    iDiff = sum * iTemp
    fan_speed = pDiff + iDiff
    if fan_speed > fan_speed_max:
        fan_speed = fan_speed_max
    if fan_speed < fan_speed_min:
        fan_speed = 0
    if sum > 100:
        sum = 100
    if sum < -100:
        sum = -100
    print("actualTemp %4.2f TempDiff %4.2f pDiff %4.2f iDiff %4.2f fan_speed %5d" % (actualTemp,diff,pDiff,iDiff,fan_speed))
    myPWM.ChangeDutyCycle(fan_speed)
    return ()


def setPin(mode):  # A little redundant function but useful if you want to add logging
    GPIO.output(fanPin, mode)
    return ()


if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(fanPin, GPIO.OUT)
        myPWM = GPIO.PWM(fanPin, 50)
        myPWM.start(50)
        GPIO.setwarnings(False)
        fanOFF()
        while True:
            handleFan()
            sleep(1)  # Read the temperature every N sec, increase or decrease this limit if you want
    except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
        fanOFF()
        GPIO.cleanup()  # resets all GPIO ports used by this program
