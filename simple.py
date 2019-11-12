from flask import Flask, escape, request, redirect, url_for
from flask_socketio import SocketIO, emit
import datetime
import threading
import time
import eventlet
import pgpubsub
import os
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def index():
    print('blablabla')
    return redirect(url_for('static', filename='index.html'))

if __name__ == '__main__':
    app.run()
    print('mark2')
