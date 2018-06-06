from .cbindings import *

import platform
import sys

if sys.version_info[0] == 2:
    range = xrange

class BleatException(Exception):
    pass

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

            options.append(_Option(key="address", value=address))
            if ('hci' in kwargs and platform.system() == 'Linux'):
                options.append(_Option(key="hci", value=kwargs['hci']))
            if ('addr_type' in kwargs):
                options.append(_Option(key="addr_type", value=kwargs['addr_type']))

            coptions = (_Option * len(options))
            for i in range(0, len(options)):
                coptions[i] = options[i]

            self.gatt = libbleat.bleat_gatt_create_with_options(len(options), coptions)
        else:
            self.gatt = libbleat.bleat_gatt_create(address)

        self.characteristics = {}

    def __del__(self):
        libbleat.bleat_gatt_delete(self.gatt)
        self.characteristics = {}

    def connect_async(self, handler):
        def completed(ctx, caller, msg):
            if (msg == None):
                handler(None)
            else:
                handler(BleatException(msg))

        self.connect_handler = FnVoid_VoidP_BleatGattP_CharP(completed)
        libbleat.bleat_gatt_connect_async(self.gatt, None, self.connect_handler)

    def disconnect(self):
        libbleat.bleat_gatt_disconnect(self.gatt)

    def on_disconnect(self, handler):
        def event_fired(ctx, gattchar, status):
            self.characteristics = {}
            handler(status)

        self.disconnect_handler = FnVoid_VoidP_BleatGattP_Int(event_fired)
        libbleat.bleat_gatt_on_disconnect(self.gatt, None, self.disconnect_handler)

    def find_characteristic(self, uuid):
        if (uuid not in self.characteristics):
            result = libbleat.bleat_gatt_find_characteristic(self.gatt, uuid)
            self.characteristics[uuid] = GattChar(self, result) if bool(result) else None
        return self.characteristics[uuid]

    def service_exists(self, uuid):
        return libbleat.bleat_gatt_has_service(self.gatt, uuid) != 0

class GattChar:
    @staticmethod
    def to_ubyte_pointer(bytes):
        arr = (c_ubyte * len(bytes))()
        i = 0
        for b in bytes:
            arr[i] = b
            i = i + 1

        return arr

    def __init__(self, owner, bleat_char):
        self.bleat_char = bleat_char
        self.owner = owner

    @property
    def uuid(self):
        return libbleat.bleat_gattchar_get_uuid(self.bleat_char).encode("ascii")

    @property
    def gatt(self):
        return self.owner

    def _private_write_async(self, fn, value, handler):
        def completed(ctx, caller, msg):
            if (msg == None):
                handler(None)
            else:
                handler(BleatException(msg))
        self.write_handler = FnVoid_VoidP_BleatGattCharP_CharP(completed)

        array = GattChar.to_ubyte_pointer(value)
        fn(self.bleat_char, array, len(value), None, self.write_handler)

    def write_async(self, value, handler):
        self._private_write_async(libbleat.bleat_gattchar_write_async, value, handler)
        
    def write_without_resp_async(self, value, handler):
        self._private_write_async(libbleat.bleat_gattchar_write_without_resp_async, value, handler)

    def read_value_async(self, handler):
        def completed(ctx, caller, pointer, length, msg):
            if (msg == None):
                value= cast(pointer, POINTER(c_ubyte * length))
                handler([value.contents[i] for i in range(0, length)], None)
            else:
                handler(None, BleatException(msg))
        self.read_handler = FnVoid_VoidP_BleatGattCharP_UbyteP_Ubyte_CharP(completed)

        libbleat.bleat_gattchar_read_async(self.bleat_char, None, self.read_handler)

    def _private_edit_notifications(self, fn, handler):
        def completed(ctx, caller, msg):
            if (msg == None):
                handler(None)
            else:
                handler(BleatException(msg))
        self.enable_handler = FnVoid_VoidP_BleatGattCharP_CharP(completed)

        fn(self.bleat_char, None, self.enable_handler)

    def enable_notifications_async(self, handler):
        self._private_edit_notifications(libbleat.bleat_gattchar_enable_notifications_async, handler)
        
    def disable_notifications_async(self, handler):
        self._private_edit_notifications(libbleat.bleat_gattchar_disable_notifications_async, handler)

    def set_value_changed_handler(self, handler):
        def value_converter(ctx, caller, pointer, length):
            value= cast(pointer, POINTER(c_ubyte * length))
            handler([value.contents[i] for i in range(0, length)])
        self.value_changed_wrapper = FnVoid_VoidP_BleatGattCharP_UbyteP_Ubyte(value_converter)
        
        libbleat.bleat_gattchar_set_value_changed_handler(self.bleat_char, None, self.value_changed_wrapper)