#!/usr/bin/env python

import logging
import os
import socket
import time

import RPi.GPIO as GPIO

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

logging.basicConfig(filename='unlock_door.log', level=logging.INFO)

# Default values
UNLOCK_TIME = 2.5
FREQUENCY = 50  # Hz
SERVO_PIN = 27
DUTY_CYCLE_OPEN, DUTY_CYCLE_CLOSED = 6, 3  # in %

config_file_paths = [os.path.expanduser('~/rpi-lock.cfg'),
                     os.path.join(os.path.realpath(os.path.dirname(__file__)), "rpi-lock.cfg")]
config = configparser.ConfigParser()
config.read(config_file_paths)
try:
    DUTY_CYCLE_OPEN = int(config.get("SERVO", "OPEN"))
    DUTY_CYCLE_CLOSED = int(config.get("SERVO", "CLOSED"))
    SERVO_PIN = int(config.get("SERVO", "PIN"))
    FREQUENCY = int(config.get("SERVO", "FREQUENCY"))
except configparser.Error as err:
    logging.warning("ConfigParser error: %s", err)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, FREQUENCY)


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 5555))

    while True:
        s.listen(1)
        conn, addr = s.accept()
        message = conn.recv(1024)
        logging.info("Recieved request: %s", message.decode("utf-8"))
        if message == b"unlock":
            unlock_door()
            conn.sendall(b"Servo Triggered")
        else:
            conn.sendall(b"Improper request, not unlocking door.")


def unlock_door():
    logging.info('Unlocking...')
    servo.start(DUTY_CYCLE_OPEN)
    time.sleep(UNLOCK_TIME)
    logging.info('Locking...')
    servo.ChangeDutyCycle(DUTY_CYCLE_CLOSED)
    time.sleep(1)
    servo.ChangeDutyCycle(0)

if __name__ == '__main__':
    try:
        server()
    except KeyboardInterrupt:
        GPIO.cleanup()
