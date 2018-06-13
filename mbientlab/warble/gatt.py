from .cbindings import *
from .cbindings import _Gatt, _Option
from .gattchar import GattChar
from . import WarbleException, str_to_bytes, bytes_to_str
from ctypes import cast, POINTER

import platform

class Gatt:
    def __init__(self, mac, **kwargs):
        """
        Creates a Python Warble Gatt object
        @params:
            mac         - Required  : mac address of the board to connect to e.g. E8:C9:8F:52:7B:07
            hci         - Optional  : mac address of the hci device to use, only applicable on Linux
            addr_type   - Optional  : ble device adress type, defaults to random
        """
        
        self.gatt = cast(None, POINTER(_Gatt))
        if (len(kwargs) != 0):
            options = []

            options.append(['mac', mac])
            if ('hci' in kwargs and platform.system() == 'Linux'):
                options.append(['hci', kwargs['hci']])
            if ('addr_type' in kwargs):
                options.append(['addr_type', kwargs['addr_type']])

            coptions = (_Option * len(options))()
            for i, v in enumerate(options):
                coptions[i] = _Option(key = str_to_bytes(v[0]), value = str_to_bytes(v[1]))

            self.gatt = libwarble.warble_gatt_create_with_options(len(options), cast(coptions, POINTER(_Option)))
        else:
            self.gatt = libwarble.warble_gatt_create(str_to_bytes(mac))

        self.characteristics = {}

    def __del__(self):
        libwarble.warble_gatt_delete(self.gatt)
        self.characteristics = {}

    @property
    def is_connected(self):
        return libwarble.warble_gatt_is_connected(self.gatt) != 0

    def connect_async(self, handler):
        """
        Establishes a connection to the remote device
        @params:
            handler     - Required  : `(Exception) -> void` function that will be executed when the connect task is completed
        """
        def completed(ctx, caller, msg):
            if (msg == None):
                handler(None)
            else:
                handler(WarbleException(bytes_to_str(msg)))

        self.connect_handler = FnVoid_VoidP_WarbleGattP_CharP(completed)
        libwarble.warble_gatt_connect_async(self.gatt, None, self.connect_handler)

    def disconnect(self):
        """
        Closes the connection with the remote device
        """
        libwarble.warble_gatt_disconnect(self.gatt)

    def on_disconnect(self, handler):
        """
        Sets a handler to listen for disconnect events
        @params:
            handler     - Required  : `(int) -> void` function that will be executed when connection is lost
        """
        def event_fired(ctx, caller, status):
            self.characteristics = {}
            handler(status)

        self.disconnect_handler = FnVoid_VoidP_WarbleGattP_Int(event_fired)
        libwarble.warble_gatt_on_disconnect(self.gatt, None, self.disconnect_handler)

    def find_characteristic(self, uuid):
        """
        Find the GATT characteristic corresponding to the uuid value
        @params:
            uuid        - Required  : 128-bit UUID string to search for
        """
        if (uuid not in self.characteristics):
            result = libwarble.warble_gatt_find_characteristic(self.gatt, str_to_bytes(uuid))
            self.characteristics[uuid] = GattChar(self, result) if bool(result) else None
        return self.characteristics[uuid]

    def service_exists(self, uuid):
        """
        Check if a GATT service with the corresponding UUID exists on the device
        @params:
            uuid        - Required  : 128-bit UUID string to search for
        """
        return libwarble.warble_gatt_has_service(self.gatt, str_to_bytes(uuid)) != 0
