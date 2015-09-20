#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os
import os.path
import httplib
import subprocess
from functools import wraps
from contextlib import closing

from flask import Flask, render_template, g, redirect, session, request, \
                flash, url_for, abort

app = Flask(__name__)

# Both paths below must be absolute
RFID_STATUS_FILE = '/tmp/rfid_running'
UNLOCK_DOOR_PATH = '/home/pi/rpi_lock/unlock_door.py'

DATABASE = 'doorlock.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# use default settings located in this file
app.config.from_object(__name__)
# overwrite default settings with file set by the env variable if set
if os.environ.get('RPI_INTERFACE_SETTINGS') != (None and ''):
    app.config.from_envvar('RPI_INTERFACE_SETTINGS')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

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
    for key, value in form_values.iteritems():
        if len(value) <= 0:
            if key != 'note':
                flash(u'{} is below min value'.format(key), 'warning')
                result = False
        if len(value) >=100:
            flash(u'{} exceeds max length'.format(key), 'warning')
            result = False
        if key == 'binary':
            for char in value:
                if char not in ('0', '1'):
                    flash(u'String "{}" is not binary'.format(value), 'warning')
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
    if form_validator(request.form) == False:
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
    cur = g.db.execute('select id, date, name, binary, status from log order by id desc limit 100')
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
        subprocess.Popen(["sudo", "python", UNLOCK_DOOR_PATH, "web"])
        flash('Unlocking Door', 'info')
    return redirect(url_for('show_log'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(405)
def page_not_found(error):
    return render_template('405.html'), 405

@app.errorhandler(400)
def page_not_found(error):
    return render_template('400.html'), 400

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=80)
