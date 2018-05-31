from ctypes import *
import os

class ScanMftData(Structure):
    _fields_ = [
        ("value", POINTER(c_ubyte)),
        ("value_size", c_int),
        ("company_id", c_ushort)
    ]

class ScanResult(Structure):
    _fields_ = [
        ("mac", c_char_p),
        ("name", c_char_p),
        ("manufacturer_data", POINTER(ScanMftData)),
        ("manufacturer_data_size", c_int),
        ("rssi", c_int)
    ]

class Gatt(Structure):
    pass

class Option(Structure):
    _fields_ = [
        ("key", c_char_p),
        ("name", c_char_p)
    ]

class GattChar(Structure):
    pass

FnVoid_VoidP_BleatGattP_CharP = CFUNCTYPE(None, c_void_p, POINTER(Gatt), c_char_p)
FnVoid_VoidP_BleatGattP_Uint = CFUNCTYPE(None, c_void_p, POINTER(Gatt), c_uint)
FnVoid_VoidP_BleatScanResultP = CFUNCTYPE(None, c_void_p, POINTER(ScanResult))
FnVoid_VoidP_BleatGattCharP_CharP = CFUNCTYPE(None, c_void_p, POINTER(GattChar), c_char_p)
FnVoid_VoidP_BleatGattCharP_UbyteC_Ubyte_CharP = CFUNCTYPE(None, c_void_p, POINTER(GattChar), POINTER(c_ubyte), c_ubyte, c_char_p)
FnVoid_VoidP_BleatGattCharP_UbyteC_Ubyte = CFUNCTYPE(None, c_void_p, POINTER(GattChar), POINTER(c_ubyte), c_ubyte)

libblepp = CDLL(os.path.join(os.path.dirname(__file__), 'libble++.so'), mode = RTLD_GLOBAL)
libbleat = CDLL(os.path.join(os.path.dirname(__file__), 'libbleat.so'))

libbleat.bleat_lib_version.restype = c_char_p
libbleat.bleat_lib_version.argtypes = None

libbleat.bleat_lib_config.restype = c_char_p
libbleat.bleat_lib_config.argtypes = None

libbleat.bleat_lib_init.restype = None
libbleat.bleat_lib_init.argtypes = [c_int, POINTER(Option)]

libbleat.bleat_scanner_configure.restype = None
libbleat.bleat_scanner_configure.argtypes = [c_int, POINTER(Option)]

libbleat.bleat_scanner_stop.restype = None
libbleat.bleat_scanner_stop.argtypes = None

libbleat.bleat_scanner_start.restype = None
libbleat.bleat_scanner_start.argtypes = None

libbleat.bleat_scanner_set_handler.restype = None
libbleat.bleat_scanner_set_handler.argtypes = [c_void_p, FnVoid_VoidP_BleatScanResultP]

libbleat.bleat_gatt_connect_async.restype = None
libbleat.bleat_gatt_connect_async.argtypes = [POINTER(Gatt), c_void_p, FnVoid_VoidP_BleatGattP_CharP]
    
libbleat.bleat_gatt_disconnect.restype = None
libbleat.bleat_gatt_disconnect.argtypes = [POINTER(Gatt)]

libbleat.bleat_gatt_delete.restype = None
libbleat.bleat_gatt_delete.argtypes = [POINTER(Gatt)]

libbleat.bleat_gatt_on_disconnect.restype = None
libbleat.bleat_gatt_on_disconnect.argtypes = [POINTER(Gatt), c_void_p, FnVoid_VoidP_BleatGattP_Uint]

libbleat.bleat_gatt_create.restype = POINTER(Gatt)
libbleat.bleat_gatt_create.argtypes = [c_char_p]

libbleat.bleat_gatt_create_with_options.restype = POINTER(Gatt)
libbleat.bleat_gatt_create_with_options.argtypes = [c_int, POINTER(Option)]

libbleat.bleat_gatt_find_characteristic.restype = POINTER(GattChar)
libbleat.bleat_gatt_find_characteristic.argtypes = [POINTER(Gatt), c_char_p]

libbleat.bleat_gattchar_disable_notifications_async.restype = None
libbleat.bleat_gattchar_disable_notifications_async.argtypes = [POINTER(GattChar), c_void_p, FnVoid_VoidP_BleatGattCharP_CharP]

libbleat.bleat_gattchar_write_without_resp_async.restype = None
libbleat.bleat_gattchar_write_without_resp_async.argtypes = [POINTER(GattChar), POINTER(c_ubyte), c_ubyte, c_void_p, FnVoid_VoidP_BleatGattCharP_CharP]

libbleat.bleat_gattchar_read_async.restype = None
libbleat.bleat_gattchar_read_async.argtypes = [POINTER(GattChar), c_void_p, FnVoid_VoidP_BleatGattCharP_UbyteC_Ubyte_CharP]

libbleat.bleat_gattchar_write_async.restype = None
libbleat.bleat_gattchar_write_async.argtypes = [POINTER(GattChar), POINTER(c_ubyte), c_ubyte, c_void_p, FnVoid_VoidP_BleatGattCharP_CharP]

libbleat.bleat_gattchar_enable_notifications_async.restype = None
libbleat.bleat_gattchar_enable_notifications_async.argtypes = [POINTER(GattChar), c_void_p, FnVoid_VoidP_BleatGattCharP_CharP]

libbleat.bleat_gattchar_set_value_changed_handler.restype = None
libbleat.bleat_gattchar_set_value_changed_handler.argtypes = [POINTER(GattChar), c_void_p, FnVoid_VoidP_BleatGattCharP_UbyteC_Ubyte]

