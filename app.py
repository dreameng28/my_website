# coding: utf-8
from flask import Flask
from flask import render_template, request
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
def index():
    ip = request.remote_addr
    agent = str(request.user_agent)
    click_info = ClickInfo()
    click_info.set('click_ip', ip)
    click_info.set('click_agent', agent)
    if 'Android' in agent:
        system = 'Android'
    elif 'Macintosh' in agent:
        system = 'Mac'
    elif 'iPhone' in agent:
        system = 'iPhone'
    elif 'windows' or 'Windows' in agent:
        system = 'Windows'
    else:
        system = 'other'
    click_info.set('system', system)
    click_info.save()
    query = leancloud.Query(ClickInfo)
    count = query.count()
    return render_template('index.html', count=count, info=system)

