from mbientlab.warble import *
from time import sleep
from threading import Event

e = Event()

print(sys.argv[1])

def connect_completed(err):
    if (err != None):
        print("connect failed: %s" % err)
    else:
        print("connected")
    e.set()

gatt = Gatt(sys.argv[1])
gatt.connect_async(connect_completed)
e.wait()

sleep(5.0)

gatt.disconnect()
print("disconnected")