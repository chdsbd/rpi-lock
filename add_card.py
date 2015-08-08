#!/usr/bin/env python2
from __future__ import print_function

from datetime import datetime
import os
import sqlite3

db_path = 'card_database.db'

def select_binary():
    con = sqlite3.connect(db_path)
    with con:
        cur = con.cursor()
        cur.execute('''SELECT Binary, Date FROM log ORDER BY Name
                       DESC LIMIT 1''')
        binary_id = cur.fetchall()
        return binary_id[0]

def auth_card(binary, name, status):
    con = sqlite3.connect(db_path)
    with con:
        cur = con.cursor()
        cur.execute('''SELECT EXISTS (SELECT 1 FROM cardlist
                       WHERE Binary=?)''', [binary]
                                            )
        existing_data = cur.fetchall()
        if existing_data[0][0] != 0:
            cur.execute('''UPDATE cardlist SET Name=?, Status=?, Date=?
                           WHERE Binary=?''', [name,
                                               status,
                                               datetime.utcnow(),
                                               binary]
                                               )
            con.commit()
        else:
            cur.execute('''INSERT INTO cardlist (Date, Binary, Name, Status)
                           VALUES(?,?,?,?)''', [datetime.utcnow(),
                                                binary,
                                                name,
                                                status]
                                                )
            con.commit()

    print('Finished.')

def user_setup():
    try:
        os.environ['SUDO_GID']
    except KeyError:
        raise Exception('This script MUST be run as root (sudo)')
    print('This script will use the lastest card read data from the rfid reader.')
    print('If card already exists in table, data will be OVERWRITTEN!')
    print('Please scan card before continuing if you have not done so already.\n')
    raw_input('Hit Ctrl-C at any time to cancel. \nHit ENTER to continue.')

    date = select_binary()[1]
    binary = select_binary()[0]

    print('\nUsing ID from last read at {}.'.format(date))
    raw_input('\nHit ENTER to continue.')

    print('\nBinary:', binary)
    raw_input('\nHit ENTER to continue.')

    name = raw_input('\nCard Holder Name: ')
    print('Card Holder Name Accepted as:', name)

    status = raw_input('\nAllow entry (Yes/no): ')
    if status in ['No', 'no']:
        entry_status = False
    else:
        entry_status = True

    print('Allow status set to:', str(entry_status))
    print('\nContinue with Binary: {}, Name: {}, Entry Status: {}?\n'.format(
                                                                      binary,
                                                                      name,
                                                                      entry_status))
    raw_input('Hit ENTER to continue. CTRL-C to escape.')
    auth_card(binary, name, entry_status)

if __name__ == '__main__':
    if os.path.isfile(db_path):
        user_setup()
    else:
        print('Database is missing!')
