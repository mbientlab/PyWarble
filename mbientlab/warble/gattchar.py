from .cbindings import *
from . import WarbleException, bytes_to_str

import sys

if sys.version_info[0] == 2:
    range = xrange

class GattChar:
    @staticmethod
    def _to_ubyte_pointer(bytes):
        arr = (c_ubyte * len(bytes))()
        i = 0
        for b in bytes:
            arr[i] = b
            i = i + 1

        return arr

    def __init__(self, owner, warble_char):
        """
        Creates a Python Warble GattChar object
        @params:
            owner       - Required  : Parent object this GattChar object belongs to
            warble_char  - Required  : Pointer to the underlying ctypes _GattChar object
        """
        self.warble_char = warble_char
        self.owner = owner

    @property
    def uuid(self):
        """
        128-bit UUID string identifying this GATT characteristic
        """
        return bytes_to_str(libwarble.warble_gattchar_get_uuid(self.warble_char))

    @property
    def gatt(self):
        """
        Parent Gatt object that self belongs to
        """
        return self.owner

    def _private_write_async(self, fn, value, handler):
        def completed(ctx, caller, msg):
            if (msg == None):
                handler(None)
            else:
                handler(WarbleException(bytes_to_str(msg)))
        self.write_handler = FnVoid_VoidP_WarbleGattCharP_CharP(completed)

        array = GattChar._to_ubyte_pointer(value)
        fn(self.warble_char, array, len(value), None, self.write_handler)

    def write_async(self, value, handler):
        """
        Writes value to the characteristic requiring an acknowledge from the remote device
        @params:
            value       - Required  : Bytes to write to the characteristic
            handler     - Required  : `(Exception) -> void` function that is executed when the write operation is done
        """
        self._private_write_async(libwarble.warble_gattchar_write_async, value, handler)
        
    def write_without_resp_async(self, value, handler):
        """
        Writes value to the characteristic without requesting a response from the remove device
        @params:
            value       - Required  : Bytes to write to the characteristic
            handler     - Required  : `(Exception) -> void` function that is executed when the write operation is done
        """
        self._private_write_async(libwarble.warble_gattchar_write_without_resp_async, value, handler)

    def read_value_async(self, handler):
        """
        Reads current value from the characteristic
        @params:
            handler     - Required  : `(array, Exception) -> void` function that is executed when the read operation is done
        """
        def completed(ctx, caller, pointer, length, msg):
            if (msg == None):
                value= cast(pointer, POINTER(c_ubyte * length))
                handler([value.contents[i] for i in range(0, length)], None)
            else:
                handler(None, WarbleException(bytes_to_str(msg)))
        self.read_handler = FnVoid_VoidP_WarbleGattCharP_UbyteP_Ubyte_CharP(completed)

        libwarble.warble_gattchar_read_async(self.warble_char, None, self.read_handler)

    def _private_edit_notifications(self, fn, handler):
        def completed(ctx, caller, msg):
            if (msg == None):
                handler(None)
            else:
                handler(WarbleException(bytes_to_str(msg)))
        self.enable_handler = FnVoid_VoidP_WarbleGattCharP_CharP(completed)

        fn(self.warble_char, None, self.enable_handler)

    def enable_notifications_async(self, handler):
        """
        Enables characteristic notifications 
        @params:
            handler     - Required  : `(Exception) -> void` function that is executed when the enable operation is done
        """
        self._private_edit_notifications(libwarble.warble_gattchar_enable_notifications_async, handler)
        
    def disable_notifications_async(self, handler):
        """
        Disables characteristic notifications 
        @params:
            handler     - Required  : `(Exception) -> void` function that is executed when the disable operation is done
        """
        self._private_edit_notifications(libwarble.warble_gattchar_disable_notifications_async, handler)

    def on_notification_received(self, handler):
        """
        Assigns a handler for characteristic notifications
        @params:
            handler     - Required  : `(array) -> void` function that all received values is forwarded to
        """
        def value_converter(ctx, caller, pointer, length):
            value= cast(pointer, POINTER(c_ubyte * length))
            handler([value.contents[i] for i in range(0, length)])
        self.value_changed_wrapper = FnVoid_VoidP_WarbleGattCharP_UbyteP_Ubyte(value_converter)
        
        libwarble.warble_gattchar_on_notification_received(self.warble_char, None, self.value_changed_wrapper)
