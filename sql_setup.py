#!/usr/bin/env python

from contextlib import closing
import os
import sqlite3

DATABASE = 'doorlock.db'

# SQL must be setup as user so table is editable by user

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    with closing(connect_db()) as db:
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    try:
        os.environ['SUDO_GID']
    except KeyError:
        init_db()
