from mbientlab.warble import *
from time import sleep


def scan_result_printer(result):
    print("mac: %s" % result.mac)
    print("name: %s" % result.name)
    print("rssi: %ddBm" % result.rssi)

    print("metawear service? %d" % result.has_service_uuid("326a9000-85cb-9195-d9dd-464cfbbae75a"))
    
    data = result.get_manufacturer_data(0x626d)
    if data != None:
        print("mbientlab manufacturer data? ")
        print("    value: [%s]" % (', '.join([("0x%02x" % d) for d in data])))
    else:
        print("mbientlab manufacturer data? false")
    print("======")
    
BleScanner.set_handler(scan_result_printer)

print("-- active scan --")
BleScanner.start()
sleep(5.0)
BleScanner.stop()

print("-- passive scan --")
BleScanner.start(**{'scan_type': 'passive'})
sleep(5.0)
BleScanner.stop()