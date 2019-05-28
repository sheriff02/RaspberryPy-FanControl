#!/usr/bin/env python3
# Authors: Sheriff02, GusevMihail
# Based on idea of: Andreas Spies
import os
# import time
from time import sleep
# import signal
# import sys
import RPi.GPIO as GPIO
from collections import deque

# Settings
fanPin = 18  # The pin ID, edit here to change it
desiredTemp = 54  # The maximum temperature in Celsius after which we trigger the fan and work to "return" to it
fan_speed_min = 20  # Minimal speed of fan, if more lower - going off. Because most of fans very loud on low PWM
fan_speed_max = 100  # Maximum speed of fan

pTemp = 20  # Proportional coef. of PI(D)
iTemp = 0.1  # Integral coef. of PI(D)
output_buffer_length = 10  # Buffer for more stable fan speed

output_buffer = deque(maxlen=output_buffer_length)


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp = (res.replace("temp=", "").replace("'C\n", ""))
    # print("temp is {0}".format(temp)) #Uncomment here for testing
    return float(temp)


def fanOFF():
    myPWM.ChangeDutyCycle(0)  # switch fan off
    return ()


def average(iterable):
    return sum(iterable) / len(iterable)


class PID:
    def __init__(self, current_value, target_value, p_coeff=1.0, i_coeff=0.0, d_coeff=0.0, is_average_out: bool = False,
                 len_average_out=10, i_buff_min=-100, i_buff_max=100, out_min=0, out_max=100):
        self.current_value = current_value
        self.target_value = target_value
        self.p_coeff = p_coeff
        self.i_coeff = i_coeff
        self.d_coeff = d_coeff
        self.is_average_out = is_average_out
        self.len_average_out = len_average_out
        self.i_buff_min = i_buff_min
        self.i_buff_max = i_buff_max
        self.out_min = out_min
        self.out_max = out_max
        self.i_buffer = 0.0
        self.out_buffer = deque(maxlen=len_average_out)
        self.reg_error = 0
        self.p_value = 0
        self.i_value = 0
        self.d_value = 0
        self.out = 0

    @staticmethod
    def _average(iterable):
        return sum(iterable) / len(iterable)

    @staticmethod
    def _limits(number, lower_limit, upper_limit):
        if number > upper_limit:
            return upper_limit
        elif number < lower_limit:
            return lower_limit
        else:
            return number

    def output(self):
        self.reg_error = self.current_value - self.target_value
        self.p_value = self.p_coeff * self.reg_error
        self.i_buffer = self._limits(self.i_buffer + self.reg_error, self.i_buff_min, self.i_buff_max)
        self.i_value = self.i_coeff * self.i_buffer
        # TODO implement d-component of PID
        output = self._limits(self.p_value + self.i_value, self.out_min, self.out_max)  # + d_value

        self.out_buffer.append(output)
        if self.is_average_out:
            self.out = self._average(self.out_buffer)

        self.out = self._limits(self.out, self.out_min, self.out_max)

        return self.out

    def update(self, current_value):
        self.current_value = current_value

    def print_state(self):
        print("actualTemp %4.2f TempDiff %4.2f pDiff %4.2f iDiff %4.2f fan_speed %5d" % (
            self.current_value, self.reg_error, self.p_value, self.p_value, self.out))


fan_PID = PID(current_value=getCPUtemperature(),
              target_value=desiredTemp,
              p_coeff=pTemp, i_coeff=iTemp,
              is_average_out=True,
              len_average_out=output_buffer_length,
              i_buff_min=-100,
              i_buff_max=100,
              out_min=fan_speed_min,
              out_max=fan_speed_max)


def handleFan(PID):
    PID.update(getCPUtemperature())
    fan_speed = PID.output()
    myPWM.ChangeDutyCycle(fan_speed)
    PID.print_state()  # print statistic in console
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
        fan_PID = PID(current_value=getCPUtemperature(),
                      target_value=desiredTemp,
                      p_coeff=pTemp, i_coeff=iTemp,
                      is_average_out=True,
                      len_average_out=output_buffer_length)
        while True:
            handleFan(fan_PID)
            sleep(1)  # Read the temperature every N sec, increase or decrease this limit if you want
    except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
        fanOFF()
        GPIO.cleanup()  # resets all GPIO ports used by this program
