#!/usr/bin/env python
from __future__ import print_function

import time

from RPIO import PWM

servo = PWM.Servo()

def unlock_door():
    while True:
        print('500')
        servo.set_servo(27, 1300)
        time.sleep(4)
        print('2300')
        servo.set_servo(27, 1500)
        time.sleep(4)

if __name__ == '__main__':
    try:
        unlock_door()
    except:
        servo.stop_servo(27)
