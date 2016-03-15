#!/usr/bin/env python

import logging
import os
import socket
import sqlite3
import time
from datetime import datetime

import RPi.GPIO as GPIO

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

logging.basicConfig(filename='read_process.log', level=logging.INFO)

# Default values
DATA0 = 11
DATA1 = 7
database = os.path.join(os.path.realpath(
    os.path.dirname(__file__)), "doorlock.db")
BASE_TIMEOUT = 10
RFID_STATUS_FILE = "/tmp/rfid_running"

config_file_paths = [os.path.expanduser('~/rpi-lock.cfg'),
                     os.path.join(os.path.realpath(os.path.dirname(__file__)), "rpi-lock.cfg")]
config = configparser.ConfigParser()
config.read(config_file_paths)
try:
    DATA0 = int(config.get("RFID", "DATA0"))
    DATA1 = int(config.get("RFID", "DATA1"))
    BASE_TIMEOUT = int(config.get("RFID", "BASE_TIMEOUT"))
    RFID_STATUS_FILE = config.get("PATH", "RFID_STATUS_FILE").strip("'")
except configparser.Error as err:
    logging.warning("ConfigParser error: %s", err)

timeout = BASE_TIMEOUT
bits = ''


def gpio_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DATA0, GPIO.IN)
    GPIO.setup(DATA1, GPIO.IN)
    GPIO.add_event_detect(DATA0, GPIO.FALLING, callback=zero)
    GPIO.add_event_detect(DATA1, GPIO.FALLING, callback=one)


def connect_db():
    return sqlite3.connect(database)


def one(channel):
    global bits
    global timeout
    bits = bits + '1'
    timeout = BASE_TIMEOUT


def zero(channel):
    global bits
    global timeout
    bits = bits + '0'
    timeout = BASE_TIMEOUT


def loop():
    global timeout
    global bits
    while True:
        if len(bits) > 0:
            timeout -= 1
            if timeout == 0:
                process_card(bits)
                bits = ''
                timeout = BASE_TIMEOUT
        time.sleep(.001)


def process_card(binary):
    name, status = auth_status(binary)
    if status:
        logging.info(u'Allowed "%s" entry.', name)
        unlock()
        log(status, binary, name)
    else:
        logging.info('Disallowed: %s', binary)
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
    logging.info("Received reply to unlock request: %s", reply.decode("utf-8"))


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
        open(RFID_STATUS_FILE, 'w')
        gpio_setup()
        loop()
    except KeyboardInterrupt:
        os.remove(RFID_STATUS_FILE)
        GPIO.cleanup()
        logging.info('Clean Exit.')

if __name__ == '__main__':
    main()
