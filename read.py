#! /usr/bin/env python

import serial, sys, time, datetime

BAUD_RATE = 250000
DEVICES = [\
  '/dev/cu.usbmodem1421',\
  '/dev/cu.usbmodem1411'\
]
SLEEP_TIME_BETWEEN_CONNECTION_ATTEMPTS = 3

class NotConnectedException(Exception):
    pass

def aprint(msg):
  print("   %s >>> %s" % (datetime.datetime.now().strftime("%H:%M:%S.%f"), msg))

def read_stuff(ser):
  # values = []
  while True:
    # try:
    val = ser.readline().strip()
    aprint(val)
    # except ValueError:
    #   print("ssss")
    # if len(values) >= 1:
    #   print(values)
    #   values = []

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
      print("Arduino not connected, sleep(%d)..." % SLEEP_TIME_BETWEEN_CONNECTION_ATTEMPTS)
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
