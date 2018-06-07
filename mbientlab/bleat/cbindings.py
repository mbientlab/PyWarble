from ctypes import *

import os
import platform

class _ScanMftData(Structure):
    _fields_ = [
        ("value", POINTER(c_ubyte)),
        ("value_size", c_uint)
    ]

class _ScanResult(Structure):
    _fields_ = [
        ("mac", c_char_p),
        ("name", c_char_p),
        ("rssi", c_int),
        ("private_data", c_void_p)
    ]

class _Gatt(Structure):
    pass

class _Option(Structure):
    _fields_ = [
        ("key", c_char_p),
        ("name", c_char_p)
    ]

class _GattChar(Structure):
    pass

FnVoid_VoidP_BleatGattP_CharP = CFUNCTYPE(None, c_void_p, POINTER(_Gatt), c_char_p)
FnVoid_VoidP_BleatGattP_Int = CFUNCTYPE(None, c_void_p, POINTER(_Gatt), c_int)
FnVoid_VoidP_BleatScanResultP = CFUNCTYPE(None, c_void_p, POINTER(_ScanResult))
FnVoid_VoidP_BleatGattCharP_CharP = CFUNCTYPE(None, c_void_p, POINTER(_GattChar), c_char_p)
FnVoid_VoidP_BleatGattCharP_UbyteP_Ubyte_CharP = CFUNCTYPE(None, c_void_p, POINTER(_GattChar), POINTER(c_ubyte), c_ubyte, c_char_p)
FnVoid_VoidP_BleatGattCharP_UbyteP_Ubyte = CFUNCTYPE(None, c_void_p, POINTER(_GattChar), POINTER(c_ubyte), c_ubyte)

if (platform.system() == 'Windows'):
    libbleat = CDLL(os.path.join(os.path.dirname(__file__), 'bleat.dll'))
elif (platform.system() == 'Linux'):
    libblepp = CDLL(os.path.join(os.path.dirname(__file__), 'libble++.so'), mode = RTLD_GLOBAL)
    libbleat = CDLL(os.path.join(os.path.dirname(__file__), 'libbleat.so'))
else:
    raise RuntimeError("pybleat is not supported for the '%s' platform" % platform.system())


libbleat.bleat_lib_version.restype = c_char_p
libbleat.bleat_lib_version.argtypes = None

libbleat.bleat_lib_config.restype = c_char_p
libbleat.bleat_lib_config.argtypes = None

libbleat.bleat_lib_init.restype = None
libbleat.bleat_lib_init.argtypes = [c_int, POINTER(_Option)]

libbleat.bleat_scanner_stop.restype = None
libbleat.bleat_scanner_stop.argtypes = None

libbleat.bleat_scanner_start.restype = None
libbleat.bleat_scanner_start.argtypes = [c_int, POINTER(_Option)]

libbleat.bleat_scanner_set_handler.restype = None
libbleat.bleat_scanner_set_handler.argtypes = [c_void_p, FnVoid_VoidP_BleatScanResultP]

libbleat.bleat_scan_result_get_manufacturer_data.restype = POINTER(_ScanMftData)
libbleat.bleat_scan_result_get_manufacturer_data.argtypes = [POINTER(_ScanResult), c_ushort]

libbleat.bleat_scan_result_has_service_uuid.restype = c_int
libbleat.bleat_scan_result_has_service_uuid.argtypes = [POINTER(_ScanResult), c_char_p]

libbleat.bleat_gatt_connect_async.restype = None
libbleat.bleat_gatt_connect_async.argtypes = [POINTER(_Gatt), c_void_p, FnVoid_VoidP_BleatGattP_CharP]
    
libbleat.bleat_gatt_disconnect.restype = None
libbleat.bleat_gatt_disconnect.argtypes = [POINTER(_Gatt)]

libbleat.bleat_gatt_delete.restype = None
libbleat.bleat_gatt_delete.argtypes = [POINTER(_Gatt)]

libbleat.bleat_gatt_on_disconnect.restype = None
libbleat.bleat_gatt_on_disconnect.argtypes = [POINTER(_Gatt), c_void_p, FnVoid_VoidP_BleatGattP_Int]

libbleat.bleat_gatt_is_connected.restype = c_int
libbleat.bleat_gatt_is_connected.argtypes = [POINTER(_Gatt)]

libbleat.bleat_gatt_create.restype = POINTER(_Gatt)
libbleat.bleat_gatt_create.argtypes = [c_char_p]

libbleat.bleat_gatt_create_with_options.restype = POINTER(_Gatt)
libbleat.bleat_gatt_create_with_options.argtypes = [c_int, POINTER(_Option)]

libbleat.bleat_gatt_find_characteristic.restype = POINTER(_GattChar)
libbleat.bleat_gatt_find_characteristic.argtypes = [POINTER(_Gatt), c_char_p]

libbleat.bleat_gatt_has_service.restype = c_int
libbleat.bleat_gatt_has_service.argtypes = [POINTER(_Gatt), c_char_p]

libbleat.bleat_gattchar_disable_notifications_async.restype = None
libbleat.bleat_gattchar_disable_notifications_async.argtypes = [POINTER(_GattChar), c_void_p, FnVoid_VoidP_BleatGattCharP_CharP]

libbleat.bleat_gattchar_write_without_resp_async.restype = None
libbleat.bleat_gattchar_write_without_resp_async.argtypes = [POINTER(_GattChar), POINTER(c_ubyte), c_ubyte, c_void_p, FnVoid_VoidP_BleatGattCharP_CharP]

libbleat.bleat_gattchar_read_async.restype = None
libbleat.bleat_gattchar_read_async.argtypes = [POINTER(_GattChar), c_void_p, FnVoid_VoidP_BleatGattCharP_UbyteP_Ubyte_CharP]

libbleat.bleat_gattchar_write_async.restype = None
libbleat.bleat_gattchar_write_async.argtypes = [POINTER(_GattChar), POINTER(c_ubyte), c_ubyte, c_void_p, FnVoid_VoidP_BleatGattCharP_CharP]

libbleat.bleat_gattchar_enable_notifications_async.restype = None
libbleat.bleat_gattchar_enable_notifications_async.argtypes = [POINTER(_GattChar), c_void_p, FnVoid_VoidP_BleatGattCharP_CharP]

libbleat.bleat_gattchar_set_value_changed_handler.restype = None
libbleat.bleat_gattchar_set_value_changed_handler.argtypes = [POINTER(_GattChar), c_void_p, FnVoid_VoidP_BleatGattCharP_UbyteP_Ubyte]

libbleat.bleat_gattchar_get_uuid.restype = c_char_p
libbleat.bleat_gattchar_get_uuid.argtypes = [POINTER(_GattChar)]

libbleat.bleat_gattchar_get_gatt.restype = POINTER(_Gatt)
libbleat.bleat_gattchar_get_gatt.argtypes = [POINTER(_GattChar)]