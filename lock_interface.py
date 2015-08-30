# -*- coding: utf-8 -*-
from flask import Flask, render_template, g, redirect, session, request, flash, url_for, abort
import sqlite3
from contextlib import closing

app = Flask(__name__)

DATABASE = 'doorlock.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    cur = g.db.execute('select id, name, device, binary from users order by id desc')
    users = [dict(id=row[0], name=row[1], device=row[2], binary=row[3]) for row in cur.fetchall()]
    cur = g.db.execute('select binary from log')
    binary = cur.fetchone()
    if binary:
        binary = binary[0]
    return render_template('show_users.html', users=users, binary=binary)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_users'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_users'))

def form_validator(form_values):
    result = True
    for key, value in form_values.iteritems():
        if len(value) <=0:
            if key != 'note':
                flash(u'{} is below min value'.format(key), 'error')
                result = False
        if len(value) >=100:
            flash(u'{} exceeds max length'.format(key), 'error')
            result = False
        if key == 'binary':
            for char in value:
                if char not in ('0', '1'):
                    flash(u'String "{}" is not binary'.format(value), 'error')
                    result = False
    if result == False:
        return False

@app.route('/add', methods=['POST'])
def add_user():
    if not session.get('logged_in'):
        abort(401)
    if form_validator(request.form) == False:
        return redirect(url_for('show_users'))
    g.db.execute('insert into users (name, device, binary) values (?, ?, ?)',
                 [request.form['name'], request.form['note'], request.form['binary']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_users'))

@app.route('/delete', methods=['POST'])
def delete_user():
    if not session.get('logged_in'):
        abort(401)
    print request.form['user_id']
    g.db.execute('delete from users where id=?', [request.form['user_id']])
    g.db.commit()
    flash('User deleted successfully.')
    return redirect(url_for('show_users'))


@app.route('/log')
def show_log():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    cur = g.db.execute('select id, date, name, binary, status from log')
    log = [dict(id=row[0], date=row[1], name=row[2], binary=row[3], status=row[4]) for row in cur.fetchall()]
    return render_template('show_log.html', log=log)

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
    app.run('0.0.0.0')
