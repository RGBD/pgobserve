from flask import Flask, escape, request, redirect, url_for
from flask_socketio import SocketIO, emit
import datetime
import threading
import time
import eventlet

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
    while True:
        print('emit')
        socketio.emit('my response', {'data': str(datetime.datetime.now() )},
                broadcast=True, namespace='/test')
        eventlet.sleep(10)

eventlet.spawn(loop_report_time)

if __name__ == '__main__':
    socketio.run(app)
