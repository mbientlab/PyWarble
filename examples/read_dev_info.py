from mbientlab.warble import *

from collections import deque
from time import sleep
from threading import Event

import sys

e = Event()


print(sys.argv[1])
gatt = Gatt(sys.argv[1])
gatt.connect_async(lambda error: e.set())
e.wait()

print("connected")
e.clear()

chars = deque([
    "00002a26-0000-1000-8000-00805f9b34fb",
    "00002a24-0000-1000-8000-00805f9b34fb",
    "00002a27-0000-1000-8000-00805f9b34fb",
    "00002a29-0000-1000-8000-00805f9b34fb",
    "00002a25-0000-1000-8000-00805f9b34fb"
])
def read_gatt_chars():
    if len(chars) == 0:
        e.set()
    else:
        gattchar = gatt.find_characteristic(chars.popleft())
        if gattchar != None:
            def completed(value, error):
                if error == None:
                    print("%s: %s" % (gattchar.uuid, bytearray(value).decode('ascii')))
                    read_gatt_chars()
                else:
                    print("%s: Error reading gatt char (%s)" % (gattchar.uuid, error))

            gattchar.read_value_async(completed)
        else:
            print("%s: does not exist" % gattchar.uuid)
            read_gatt_chars()

read_gatt_chars()
e.wait()

gatt.disconnect()
print("disconnected")
