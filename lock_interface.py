#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import socket
import sqlite3
from contextlib import closing
from datetime import datetime
from functools import wraps

from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   session, url_for)

try:
    import httplib
except ImportError:
    import http.client as httplib
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


app = Flask(__name__)

USERNAME = 'admin'
PASSWORD = 'default'
SECRET_KEY = 'development key'
DEBUG = True
PORT = 5000
DATABASE = os.path.join(os.path.realpath(
    os.path.dirname(__file__)), "doorlock.db")
RFID_STATUS_FILE = '/tmp/rfid_running'

# use default settings located in this file
app.config.from_object(__name__)

config_file_paths = [os.path.expanduser('~/rpi-lock.cfg'),
                     os.path.join(os.path.realpath(os.path.dirname(__file__)), "rpi-lock.cfg")]
config = configparser.ConfigParser()
config.read(config_file_paths)
try:
    app.config.update(
        USERNAME=config.get("WEB", "USERNAME"),
        PASSWORD=config.get("WEB", "PASSWORD"),
        SECRET_KEY=config.get("WEB", "SECRET_KEY"),
        DEBUG=bool(config.get("WEB", "DEBUG")),
        PORT=int(config.get("WEB", "PORT")),
        RFID_STATUS_FILE=config.get("PATH", "RFID_STATUS_FILE"))
except configparser.Error as e:
    print("ConfigParser Error: ", e)


def connect_db():
    return sqlite3.connect(str(app.config['DATABASE']))


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.', 'warning')
            return redirect(url_for('login'))
    return wrap


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def have_internet():
    conn = httplib.HTTPConnection("www.google.com")
    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False


def form_validator(form_values):
    result = True
    for key, value in form_values.items():
        if len(value) <= 0:
            if key != 'note':
                flash('{0} is below min value'.format(
                    key).encode("utf-8"), 'warning')
                result = False
        if len(value) >= 100:
            flash('{0} exceeds max length'.format(
                key).encode("utf-8"), 'warning')
            result = False
        if key == 'binary':
            for char in value:
                if char not in ('0', '1'):
                    flash('String "{0}" is not binary'.format(
                        value).encode("utf-8"), 'warning')
                    result = False
                    break
    return result


@app.route('/')
@login_required
def show_users():
    cur = g.db.execute('''select id, name, note, binary from users
                          order by id desc''')
    users = [dict(id=row[0],
                  name=row[1],
                  note=row[2],
                  binary=row[3]) for row in cur.fetchall()]
    cur = g.db.execute('select binary from log order by id desc limit 1')
    binary = cur.fetchone()
    if binary:
        binary = binary[0]
    return render_template('show_users.html', users=users, binary=binary)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('Invalid username', 'danger')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Invalid password', 'danger')
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_users'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_users'))


@app.route('/add', methods=['POST'])
def add_user():
    if not session.get('logged_in'):
        abort(401)
    if not form_validator(request.form):
        return redirect(url_for('show_users'))
    g.db.execute('insert into users (name, note, binary) values (?, ?, ?)',
                 [request.form['name'],
                  request.form['note'],
                  request.form['binary']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_users'))


@app.route('/delete', methods=['POST'])
def delete_user():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('delete from users where id=?', [request.form['user_id']])
    g.db.commit()
    flash('User deleted successfully.')
    return redirect(url_for('show_users'))


@app.route('/log')
@login_required
def show_log():
    cur = g.db.execute('''select id, date, name, binary, status
                       from log order by id desc limit 100''')
    log = [dict(id=row[0],
                date=row[1],
                name=row[2],
                binary=row[3],
                status=row[4]) for row in cur.fetchall()]
    return render_template('show_log.html', log=log)


@app.route('/status')
@login_required
def status():
    status = dict(rfid=os.path.isfile(RFID_STATUS_FILE), net=have_internet())
    return render_template('status.html', status=status)


@app.route('/unlock', methods=['POST'])
@login_required
def unlock_door():
    if request.form['door'] == 'unlock':
        door_unlock()
        g.db.execute('''INSERT INTO log (date, name, binary, status)
                       VALUES(?,?,?,?)''',
                     (datetime.utcnow(), 'Web User', 'Button', '1'))
        g.db.commit()
        flash('Unlocking Door', 'info')
    return redirect(url_for('show_log'))


def door_unlock():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 5555))
    s.sendall(b'unlock')
    reply = s.recv(1024)
    s.close()
    print("Received reply:", reply.decode("utf-8"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405.html'), 405


@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run('0.0.0.0', port=app.config['PORT'])
