from flask import Flask, escape, request, redirect, url_for
from flask_socketio import SocketIO, emit
import datetime
import threading
import time
import eventlet
from pgnotify import await_pg_notifications
import pgpubsub

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, logger=True, engineio_logger=True)

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    socketio.emit('my response', {'data': str(datetime.datetime.now() )},
            broadcast=True, namespace='/test')
    emit('my response', {'data': 'Connected'}, broadcast=True)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

def loop_report_time():
    print('started thread')
    pubsub = pgpubsub.connect(user='oleg', database='oleg')
    pubsub.listen('channel1')
    while True:
        event = pubsub.get_event()
        while event:
            print(event.payload)
            socketio.emit('my response',
                    { 'data': "{}: {}".format(datetime.datetime.now(), event.payload) },
                    broadcast=True, namespace='/test')
            event = pubsub.get_event()
        eventlet.sleep(0.1)

eventlet.spawn(loop_report_time)

if __name__ == '__main__':
    socketio.run(app)
