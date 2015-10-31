#!/usr/bin/env python
from __future__ import print_function

from RPIO import PWM
import time
import zmq
import os
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

# Default values
servo_pin = 27
servo_range_min, servo_range_max = 800, 1400  # Left, Right (2300 Max, 500 Min)

# overwrite default settings with file set by the env variable if set
if os.environ.get('RPI_LOCK_CONFIG_PATH') != (None and ''):
    config = ConfigParser.ConfigParser()
    config.read(os.environ['RPI_LOCK_CONFIG_PATH'])
    servo_range_max = int(config.get("SERVO", "MAX"))
    servo_range_min = int(config.get("SERVO", "MIN"))
    servo_pin = int(config.get("SERVO", "PIN"))


PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
servo = PWM.Servo()


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    print("Server started.")

    while True:
        message = socket.recv()
        print("Recieved request: %s" % message)
        if message == b"unlock":
            unlock_door()
            socket.send(b"Servo Triggered")
        else:
            socket.send(b"Improper request, not unlocking door.")


def unlock_door():
    print('Unlocking...')
    servo.set_servo(servo_pin, servo_range_max)
    time.sleep(2.5)
    print('Locking...')
    servo.set_servo(servo_pin, servo_range_min)
    time.sleep(1)
    servo.stop_servo(servo_pin)


if __name__ == '__main__':
    try:
        server()
    except:
        servo.stop_servo(servo_pin)
