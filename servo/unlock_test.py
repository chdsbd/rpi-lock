#!/usr/bin/env python

import time

from RPIO import PWM

servo = PWM.Servo()

def unlock_door():
    while True:
        servo.set_servo(27, 1300)
        time.sleep(4)
        servo.set_servo(27, 1500)
        time.sleep(4)

if __name__ == '__main__':
    try:
        unlock_door()
    except:
        servo.stop_servo(27)
