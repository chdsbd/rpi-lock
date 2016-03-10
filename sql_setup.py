#!/usr/bin/env python

import os
import sqlite3
from contextlib import closing

DATABASE = os.path.join(os.path.realpath(os.path.dirname(__file__)), "doorlock.db")

# SQL must be setup as user so table is editable by user


def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():
    with closing(connect_db()) as db:
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    init_db()
