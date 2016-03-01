#!/usr/bin/env python
from __future__ import print_function

import RPi.GPIO as GPIO
import time
import socket
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# Default values
frequency = 50 # Hz
servo_pin = 27
duty_cycle_open, duty_cycle_closed = 6, 3  # in %

# overwrite default settings with file set by the env variable if set
if os.environ.get('RPI_LOCK_CONFIG_PATH') != (None and ''):
    config = configparser.ConfigParser()
    config.read(os.environ['RPI_LOCK_CONFIG_PATH'])
    duty_cycle_open = int(config.get("SERVO", "OPEN"))
    duty_cycle_closed = int(config.get("SERVO", "CLOSED"))
    servo_pin = int(config.get("SERVO", "PIN"))
    frequency = int(config.get("SERVO", "FREQUENCY"))

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

servo = GPIO.PWM(servo_pin, frequency)

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 5555))

    while True:
        s.listen(1)
        conn, addr = s.accept()
        message = conn.recv(1024)
        print("Recieved request: ", message.decode("utf-8"))
        if message == b"unlock":
            unlock_door()
            conn.sendall(b"Servo Triggered")
        else:
            conn.sendall(b"Improper request, not unlocking door.")


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
