#!/usr/bin/env python

import time

from RPIO import PWM

pin = 4  # Uses BCM numbering
servo = PWM.Servo()

def test_servo():
    servo.set_servo(pin, 500)
    # time.sleep(3)
    # servo.set_servo(pin, 700)
    # time.sleep(3)
    # servo.set_servo(pin, 900)
    # time.sleep(3)
    # servo.set_servo(pin, 1000)
    # time.sleep(3)
    # servo.set_servo(pin, 1200)
    # time.sleep(3)
    # servo.set_servo(pin, 1300)
    time.sleep(3)
    servo.set_servo(pin, 1500)
    # time.sleep(3)
    # servo.set_servo(pin, 1700)
    # time.sleep(3)
    # servo.set_servo(pin, 1900)
    # time.sleep(3)
    # servo.set_servo(pin, 2100)
    # time.sleep(3)
    # servo.set_servo(pin, 2200)
    time.sleep(3)
    servo.set_servo(pin, 2300)
    time.sleep(3)

if __name__ == '__main__':
    try:
        test_servo()
    except:
        servo.stop_servo(pin)
