#! /usr/bin/env python

import serial
import sys
import time
import datetime
import requests
import threading

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


def worker():
    try:
        r = requests.get('http://default/tick', timeout=2)
    except:
        aprint("Could not send request to cluster: %s" % r)


def read_stuff(ser):
    while True:
        val = ser.readline().strip()
        aprint(val)

        values = val.split(' at ')
        if len(values) == 2:
            peak, time = values
            for i in range(5):
                t = threading.Thread(target=worker)
                t.start()


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
            time.sleep(SLEEP_TIME_BETWEEN_CONNECTION_ATTEMPTS)
            pass

if __name__ == "__main__":
    print("Wheel of Fortune ready! Press ctrl-c to stop.\n")

    while True:
        try:
            ser = connection_loop()
            read_stuff(ser)
        except serial.serialutil.SerialException:
            print("Arduino was disconnected. Check cable.")
            pass
        except KeyboardInterrupt:
            print("\nBye bye\n")
            sys.exit(0)
