from flask import Flask, render_template, g, redirect, session, request, flash, url_for
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
    cur = g.db.execute('select name, binary, status from users order by id desc')
    users = [dict(name=row[0], binary=row[1], status=row[2]) for row in cur.fetchall()]
    return render_template('show_users.html', users=users)

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

@app.route('/add', methods=['POST'])
def add_user():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into users (name, binary, status) values (?, ?, ?)',
                 [request.form['name'], request.form['binary'], request.form['status']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_users'))

@app.route('/log')
def show_log():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    cur = g.db.execute('select date, name, binary, status from log')
    log = [dict(date=row[0], name=row[1], binary=row[2], status=row[3]) for row in cur.fetchall()]
    return render_template('show_log.html', log=log)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')
