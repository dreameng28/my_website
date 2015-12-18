# coding: utf-8
from flask import Flask
from flask import render_template, request, session, abort, flash, redirect, url_for, g
import leancloud
from leancloud import Object
import os

APP_ID = os.environ.get('LC_APP_ID', 'la9ocsQBBbVDo41nn3lW2oQo-gzGzoHsz') # 你的 app id
MASTER_KEY = os.environ.get('LC_APP_MASTER_KEY', 'RibMsUrb3rupAu0RN7jSCy8y') #  你的 master key
leancloud.init(APP_ID, master_key=MASTER_KEY)
app = Flask(__name__)
engine = leancloud.Engine(app)

class ClickInfo(Object):
    pass

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

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
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

