from .cbindings import *
from .gattchar import GattChar
from . import BleatException, str_to_bytes, bytes_to_str

class Gatt:
    def __init__(self, address, **kwargs):
        """
        Creates a Python Bleat Gatt object
        @params:
            address     - Required  : mac address of the board to connect to e.g. E8:C9:8F:52:7B:07
            hci         - Optional  : mac address of the hci device to use, only applicable on Linux
            addr_type   - Optional  : ble device adress type, defaults to random
        """
        
        if (len(kwargs) != 0):
            options = []

            options.append(_Option(key="address", value=str_to_bytes(address)))
            if ('hci' in kwargs and platform.system() == 'Linux'):
                options.append(_Option(key="hci", value=str_to_bytes(kwargs['hci'])))
            if ('addr_type' in kwargs):
                options.append(_Option(key="addr_type", value=str_to_bytes(kwargs['addr_type'])))

            coptions = (_Option * len(options))
            for i, v in enumerate(options):
                coptions[i] = v

            self.gatt = libbleat.bleat_gatt_create_with_options(len(options), coptions)
        else:
            self.gatt = libbleat.bleat_gatt_create(str_to_bytes(address))

        self.characteristics = {}

    def __del__(self):
        libbleat.bleat_gatt_delete(self.gatt)
        self.characteristics = {}

    @property
    def is_connected(self):
        return libbleat.bleat_gatt_is_connected(self.gatt) != 0

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
                handler(BleatException(bytes_to_str(msg)))

        self.connect_handler = FnVoid_VoidP_BleatGattP_CharP(completed)
        libbleat.bleat_gatt_connect_async(self.gatt, None, self.connect_handler)

    def disconnect(self):
        """
        Closes the connection with the remote device
        """
        libbleat.bleat_gatt_disconnect(self.gatt)

    def on_disconnect(self, handler):
        """
        Sets a handler to listen for disconnect events
        @params:
            handler     - Required  : `(int) -> void` function that will be executed when connection is lost
        """
        def event_fired(ctx, caller, status):
            self.characteristics = {}
            handler(status)

        self.disconnect_handler = FnVoid_VoidP_BleatGattP_Int(event_fired)
        libbleat.bleat_gatt_on_disconnect(self.gatt, None, self.disconnect_handler)

    def find_characteristic(self, uuid):
        """
        Find the GATT characteristic corresponding to the uuid value
        @params:
            uuid        - Required  : 128-bit UUID string to search for
        """
        if (uuid not in self.characteristics):
            result = libbleat.bleat_gatt_find_characteristic(self.gatt, str_to_bytes(uuid))
            self.characteristics[uuid] = GattChar(self, result) if bool(result) else None
        return self.characteristics[uuid]

    def service_exists(self, uuid):
        """
        Check if a GATT service with the corresponding UUID exists on the device
        @params:
            uuid        - Required  : 128-bit UUID string to search for
        """
        return libbleat.bleat_gatt_has_service(self.gatt, str_to_bytes(uuid)) != 0
