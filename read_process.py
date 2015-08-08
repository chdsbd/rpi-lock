#!/usr/bin/env python
from __future__ import print_function

import time
import sqlite3
import os.path
from sys import exit
from datetime import datetime

import RPi.GPIO as GPIO
from RPIO import PWM

data1 = 7  # DATA1 (White) PIN
data0 = 11  # DATA0 (Green) PIN
servo_pin = 27
servo_range = [1500, 1300]  # Left, Right (2300 Max, 500 Min)
db_path = 'card_database.db'
base_timeout = 5

timeout = base_timeout
bits = ''

PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
servo = PWM.Servo()


def gpio_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(data1, GPIO.IN)
    GPIO.setup(data0, GPIO.IN)
    GPIO.add_event_detect(data1, GPIO.FALLING, callback=one)
    GPIO.add_event_detect(data0, GPIO.FALLING, callback=zero)


def sql_setup():
    if os.path.isfile(db_path) != True:
        print('Missing Database. Run sql_setup.py script w/o root to create.')
# TODO: Simplify checking if file exists and if tables exist within
    con = sqlite3.connect(db_path)
    with con:
        try:
            cur = con.cursor()
            cur.execute('''CREATE TABLE cardlist (Date TEXT,
                                                  Binary TEXT,
                                                  Name TEXT,
                                                  Status BOOLEAN)''')
        except Exception as e:
            if str(e) == 'table cardlist already exists':
                print('cardlist table exists')
            else:
                raise
        try:
            cur = con.cursor()
            cur.execute('CREATE TABLE log (Date, EntryStatus, Name, Binary)')
        except Exception as e:
            if str(e) == 'table log already exists':
                print('Log table exists')
            else:
                raise


def one(channel):
    global bits
    global timeout
    bits = bits + '1'
    timeout = base_timeout


def zero(channel):
    global bits
    global timeout
    bits = bits + '0'
    timeout = base_timeout


def loop():
    global timeout
    global bits
    while True:
        if len(bits) > 0:
            timeout -= 1
            if timeout == 0:
                process_card(bits)
                bits = ''
                timeout = base_timeout
        time.sleep(.001)


def process_card(binary):
    name, status = auth_status(binary)
    if status == True:
        print('Allowed "{}" entry.'.format(name))
        unlock_door()
        log(status, binary, name)
    else:
        print('Disallowed:', binary)
        log(False, binary)


def auth_status(bit_query):
    con = sqlite3.connect(db_path)
    with con:
        cur = con.cursor()
        cur.execute(
            'SELECT Name, Status FROM cardlist WHERE Binary = ?', [bit_query])
        row = cur.fetchone()
        if row is None:
            return 'Unknown', False
        else:
            name, status = row
            return name, bool(status)


def log(status, binary, name=None):
    con = sqlite3.connect(db_path)
    with con:
        cur = con.cursor()
        cur.execute('''INSERT INTO log (Date, EntryStatus, Name, Binary)
                       VALUES(?,?,?,?)''', (datetime.utcnow(), status,
                                            name, binary))


def unlock_door():
    print('Unlocking...')
    servo.set_servo(servo_pin, servo_range[1])  # OPEN
    time.sleep(4)
    print('Locking...')
    servo.set_servo(servo_pin, servo_range[0])  # CLOSE
    time.sleep(1)
    servo.stop_servo(servo_pin)


def main():
    try:
        gpio_setup()
        sql_setup()
        loop()
    except KeyboardInterrupt:
        print('\nRunning GPIO Cleanup')
        GPIO.cleanup()

if __name__ == '__main__':
    main()
