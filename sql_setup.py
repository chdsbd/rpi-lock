#!/usr/bin/env python

import os
import sqlite3

db_path = 'card_database.db'

# SQL must be setup as user so table is editable by user


def sql_setup():
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

if __name__ == '__main__':
    try:
        os.environ['SUDO_GID']
    except KeyError:
        sql_setup()
