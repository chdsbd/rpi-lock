#!/usr/bin/env python
from __future__ import print_function

from datetime import datetime
import os
import sqlite3

db_path = 'card_database.db'


def user_setup():
    print(
        '''
    This script will use the lastest card read data from the rfid reader.
    If card already exists in table, data will be OVERWRITTEN!
    Please scan card before continuing if you have not done so already.\n
        ''')

    binary, date = select_binary()
    print('Using ID from last read at {}. \nBinary: {}'.format(date, binary))

    name = raw_input('\nInput Name: ')
    print('Name:', name)

    status = raw_input('\nAllow entry (Yes/no): ')
    if status in ['No', 'no']:
        entry_status = False
    else:
        entry_status = True

    print('Entry status set to:', entry_status)
    raw_input('Hit ENTER to input data. CTRL-C to escape.')
    auth_card(binary, name, entry_status)


def select_binary():
    con = sqlite3.connect(db_path)
    with con:
        cur = con.cursor()
        cur.execute('''SELECT Binary, Date FROM log ORDER BY Name
                       DESC LIMIT 1''')
        binary_id = cur.fetchone()
        return binary_id


def auth_card(binary, name, status):
    con = sqlite3.connect(db_path)
    with con:
        cur = con.cursor()
        cur.execute('''SELECT EXISTS (SELECT 1 FROM cardlist
                       WHERE Binary=?)''', [binary]
                    )
        existing_data = cur.fetchone()
        if existing_data[0] != 0:
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
    print('Done')

if __name__ == '__main__':
    if os.path.isfile(db_path):
        user_setup()
    else:
        print('Database is missing!')
