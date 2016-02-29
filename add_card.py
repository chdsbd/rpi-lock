#!/usr/bin/env python
from __future__ import print_function

import os
import sqlite3
import click


@click.command()
@click.option('--db', default='doorlock.db', help='path to database')
@click.option('--note', default=None, help='user note')
@click.option('--binary', default=None, type=(int), help='binary data string')
@click.argument('name')
def add_user(name, db, note, binary):
    """Adds new user to database

    Arguement:
    name - Name for user in database

    Optional Arguments:
    --db - Specify database file (default 'doorlock.db')
    --note - Specify note for user (default 'none')
    --binary - Specify binary card data (default most recent attempt in log table)
    """
    if os.path.isfile(db):
        if binary is None:
            con = sqlite3.connect(db)
            with con:
                cur = con.cursor()
                cur.execute('select binary from log')
                row = cur.fetchone()
                binary = row[0]
                if binary is None:
                    print('Missing log data, use --binary argument/ update table')
                    exit(0)
        con = sqlite3.connect(db)
        with con:
            cur = con.cursor()
            cur.execute('''INSERT OR REPLACE INTO users (name, note, binary)
                           VALUES (?,?,?)''', [name, note, binary])
            con.commit()
            print(u'Added User with Name: {}, Note: {}, Binary: {}'.format(
                name, note, binary))
    else:
        print('Missing Database')


if __name__ == '__main__':
    add_user()
