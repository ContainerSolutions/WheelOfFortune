#! /usr/bin/env python

import serial, sys, time

BAUD_RATE = 250000
DEVICES = [\
  '/dev/cu.usbmodem1421',\
  '/dev/cu.usbmodem1411'\
]

class NotConnectedException(Exception):
    pass

def aprint(msg):
  print(">>> %s" % msg)

def connect():
  for device in DEVICES:
    try:
      return serial.Serial(device, BAUD_RATE)
    except OSError:
      pass
  raise(NotConnectedException)

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

def connection_loop():
  while True:
    try:
      return connect()
    except NotConnectedException:
      print("Arduino not connected, sleeping...")
      # sys.stdout.flush()
      time.sleep(1)
      pass

if __name__ == "__main__":
  print("Ready!")

  while True:
    try:
      ser = connection_loop()
      read_stuff(ser)
    except KeyboardInterrupt:
      print("Bye bye")
      sys.exit(0)
    except serial.serialutil.SerialException:
      print("Arduino was disconnected. Check cable.")
      pass
