# coding: utf-8
from flask import Flask
from flask import render_template, request, session, abort, flash, redirect, url_for, g
import leancloud
from leancloud import Object
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
engine = leancloud.Engine(app)
APP_ID = os.environ.get('LC_APP_ID', 'la9ocsQBBbVDo41nn3lW2oQo-gzGzoHsz') # 你的 app id
MASTER_KEY = os.environ.get('LC_APP_MASTER_KEY', 'RibMsUrb3rupAu0RN7jSCy8y') #  你的 master key
leancloud.init(APP_ID, master_key=MASTER_KEY)

class ClickInfo(Object):
    pass


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def user(name):
    return render_template('user.html', name=name)