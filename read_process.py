#!/usr/bin/env python
from __future__ import print_function

import time
import sqlite3
import os
from datetime import datetime

import socket
import RPi.GPIO as GPIO
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# Default values
data0 = 11
data1 = 7
database = os.path.join(os.path.realpath(os.path.dirname(__file__)), "doorlock.db")
base_timeout = 10
rfid_status_file = "/tmp/rfid_running"

config_file_paths = [os.path.expanduser('~/rpi-lock.cfg'),
                     os.path.join(os.path.realpath(os.path.dirname(__file__)), "rpi-lock.cfg")]
config = configparser.ConfigParser()
config.read(config_file_paths)
try:
    data0 = config.getint("RFID", "DATA0")
    data1 = config.getint("RFID", "DATA1")
    base_timeout = config.getint("RFID", "BASE_TIMEOUT")
    rfid_status_file = config.get("PATH", "RFID_STATUS_FILE").strip("'")
except configparser.Error as e:
    print("ConfigParser Error: ", e)

timeout = base_timeout
bits = ''


def gpio_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(data1, GPIO.IN)
    GPIO.setup(data0, GPIO.IN)
    GPIO.add_event_detect(data1, GPIO.FALLING, callback=one)
    GPIO.add_event_detect(data0, GPIO.FALLING, callback=zero)


def connect_db():
    return sqlite3.connect(database)


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
    print('Ready')
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
    if status:
        print(u'Allowed "{}" entry.'.format(name))
        unlock()
        log(status, binary, name)
    else:
        print('Disallowed:', binary)
        log(False, binary)


def auth_status(bit_query):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute(
            'SELECT name FROM users WHERE Binary = ?', [bit_query])
        row = cur.fetchone()
        if row is None:
            return row, False
        else:
            return row[0], True


def unlock():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 5555))
    s.sendall(b'unlock')
    reply = s.recv(1024)
    s.close()
    print("Received reply:", reply.decode("utf-8"))


def log(status, binary, name=None):
    if len(binary) < 10:
        pass
    else:
        con = connect_db()
        with con:
            cur = con.cursor()
            cur.execute('''INSERT INTO log (date, name, binary, status)
                           VALUES(?,?,?,?)''',
                        (datetime.utcnow(), name, binary, status))


def main():
    try:
        open(rfid_status_file, 'w')
        gpio_setup()
        loop()
    except KeyboardInterrupt:
        os.remove(rfid_status_file)
        GPIO.cleanup()
        print('Clean Exit.')

if __name__ == '__main__':
    main()
