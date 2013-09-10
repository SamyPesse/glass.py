import os
import sys

# add dist to path for buildout-managed dependencies
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dist'))

import glass
import config
import logging
from flask import session, render_template, redirect

app = glass.Application(
    name=config.appname,
    client_id=config.client_id,
    client_secret=config.client_secret)

# Set the secret key for flask session.  keep this really secret: (but here it's not ;) )
app.web.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.prepare(port=8765)

@app.web.route("/")
def index():
    configured = config.appname and config.client_id and config.client_secret
    user = None
    if 'token' in session:
        user = glass.User(app=app, token=session['token'])
    return render_template("index.html", user=user, configured=configured)

@app.subscriptions.login
def login(user):
    session['token'] = user.token
    user.timeline.post(text="Hello from App Engine!")
    return redirect('/')
