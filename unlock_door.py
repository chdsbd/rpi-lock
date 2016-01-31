#!/usr/bin/env python
from __future__ import print_function

import RPi.GPIO as GPIO
import time
import zmq
import os
try:
    import ConfigParser
except ImportError:
    import configparser

# Default values
frequency = 50 # Hz
servo_pin = 27
duty_cycle_open, duty_cycle_closed = 6, 3  # in %

# overwrite default settings with file set by the env variable if set
if os.environ.get('RPI_LOCK_CONFIG_PATH') != (None and ''):
    config = ConfigParser.ConfigParser()
    config.read(os.environ['RPI_LOCK_CONFIG_PATH'])
    duty_cycle_open = int(config.get("SERVO", "OPEN"))
    duty_cycle_closed = int(config.get("SERVO", "CLOSED"))
    servo_pin = int(config.get("SERVO", "PIN"))
    frequency = int(config.get("SERVO", "FREQUENCY"))

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

servo = GPIO.PWM(servo_pin, frequency)

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
    servo.start(duty_cycle_open)
    time.sleep(2.5)
    print('Locking...')
    servo.ChangeDutyCycle(duty_cycle_closed)
    time.sleep(1)
    servo.ChangeDutyCycle(0)

if __name__ == '__main__':
    try:
        server()
    except KeyboardInterrupt:
        GPIO.cleanup()
    except:
        GPIO.cleanup()
