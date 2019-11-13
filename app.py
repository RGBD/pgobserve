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
socketio = SocketIO(app, logger=True, engineio_logger=True)

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

def loop_report_time():
    pubsub = pgpubsub.connect(
            host=os.getenv('DATABASE_HOST'), 
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            )
    pubsub.listen('users_change')
    while True:
        event = pubsub.get_event()
        while event:
            print(event.payload)
            socketio.emit('users_change',
                    { 'data': "{}: {}".format(datetime.datetime.now(), event.payload) },
                    broadcast=True)
            event = pubsub.get_event()
        eventlet.sleep(0.1)

if __name__ == '__main__':
    eventlet.spawn(loop_report_time)
    socketio.run(app, host='0.0.0.0')
