#!/usr/bin/env python3

import eventlet
eventlet.monkey_patch()

from time import sleep
from threading import Thread
from flask import Flask
from flask_socketio import SocketIO, emit

import serial
import sys
import datetime
import threading


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')
thread = None


BAUD_RATE = 250000
DEVICES = [
    '/dev/cu.usbmodem1421',
    '/dev/cu.usbmodem1411'
]
SLEEP_TIME_BETWEEN_CONNECTION_ATTEMPTS = 3


class NotConnectedException(Exception):
    pass


def aprint(msg):
    print("   %s >>> %s" %
          (datetime.datetime.now().strftime("%H:%M:%S.%f"), msg))


def read_stuff(ser):
    while True:
        val = ser.readline().strip()
        aprint(val)
        socketio.emit('change colors',
                      {'data': 'toe maar'},
                      namespace='/test', broadCast = True)
        sleep(0.1)


def connect():
    for device in DEVICES:
        try:
            ser = serial.Serial(device, BAUD_RATE)
            print("Found Arduino at device %s" % device)
            return ser
        except OSError:
            pass
    raise(NotConnectedException)


def connection_loop():
    while True:
        try:
            return connect()
        except NotConnectedException:
            print("Arduino not connected, sleep(%d)..." %
                  SLEEP_TIME_BETWEEN_CONNECTION_ATTEMPTS)
            sys.stdout.flush()
            sleep(SLEEP_TIME_BETWEEN_CONNECTION_ATTEMPTS)
            pass

def background_thread():
    try:
        ser = connection_loop()
        read_stuff(ser)
    except serial.serialutil.SerialException:
        print("Arduino was disconnected. Check cable.")
        pass
    except KeyboardInterrupt:
        print("\nBye bye\n")
        sys.exit(0)

if __name__ == "__main__":
    print("Wheel of Fortune ready! Press ctrl-c to stop.\n")

    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    socketio.run(app, debug=True)
