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
        ("value", c_char_p)
    ]

class _GattChar(Structure):
    pass

FnVoid_VoidP_WarbleGattP_CharP = CFUNCTYPE(None, c_void_p, POINTER(_Gatt), c_char_p)
FnVoid_VoidP_WarbleGattP_Int = CFUNCTYPE(None, c_void_p, POINTER(_Gatt), c_int)
FnVoid_VoidP_WarbleScanResultP = CFUNCTYPE(None, c_void_p, POINTER(_ScanResult))
FnVoid_VoidP_WarbleGattCharP_CharP = CFUNCTYPE(None, c_void_p, POINTER(_GattChar), c_char_p)
FnVoid_VoidP_WarbleGattCharP_UbyteP_Ubyte_CharP = CFUNCTYPE(None, c_void_p, POINTER(_GattChar), POINTER(c_ubyte), c_ubyte, c_char_p)
FnVoid_VoidP_WarbleGattCharP_UbyteP_Ubyte = CFUNCTYPE(None, c_void_p, POINTER(_GattChar), POINTER(c_ubyte), c_ubyte)

if (platform.system() == 'Windows'):
    libwarble = CDLL(os.path.join(os.path.dirname(__file__), 'warble.dll'))
elif (platform.system() == 'Linux'):
    libwarble = CDLL(os.path.join(os.path.dirname(__file__), 'libwarble.so'))
else:
    raise RuntimeError("pywarble is not supported for the '%s' platform" % platform.system())

libwarble.warble_lib_version.restype = c_char_p
libwarble.warble_lib_version.argtypes = None

libwarble.warble_lib_config.restype = c_char_p
libwarble.warble_lib_config.argtypes = None

libwarble.warble_lib_init.restype = None
libwarble.warble_lib_init.argtypes = [c_int, POINTER(_Option)]

libwarble.warble_scanner_stop.restype = None
libwarble.warble_scanner_stop.argtypes = None

libwarble.warble_scanner_start.restype = None
libwarble.warble_scanner_start.argtypes = [c_int, POINTER(_Option)]

libwarble.warble_scanner_set_handler.restype = None
libwarble.warble_scanner_set_handler.argtypes = [c_void_p, FnVoid_VoidP_WarbleScanResultP]

libwarble.warble_scan_result_get_manufacturer_data.restype = POINTER(_ScanMftData)
libwarble.warble_scan_result_get_manufacturer_data.argtypes = [POINTER(_ScanResult), c_ushort]

libwarble.warble_scan_result_has_service_uuid.restype = c_int
libwarble.warble_scan_result_has_service_uuid.argtypes = [POINTER(_ScanResult), c_char_p]

libwarble.warble_gatt_connect_async.restype = None
libwarble.warble_gatt_connect_async.argtypes = [POINTER(_Gatt), c_void_p, FnVoid_VoidP_WarbleGattP_CharP]
    
libwarble.warble_gatt_disconnect.restype = None
libwarble.warble_gatt_disconnect.argtypes = [POINTER(_Gatt)]

libwarble.warble_gatt_delete.restype = None
libwarble.warble_gatt_delete.argtypes = [POINTER(_Gatt)]

libwarble.warble_gatt_on_disconnect.restype = None
libwarble.warble_gatt_on_disconnect.argtypes = [POINTER(_Gatt), c_void_p, FnVoid_VoidP_WarbleGattP_Int]

libwarble.warble_gatt_is_connected.restype = c_int
libwarble.warble_gatt_is_connected.argtypes = [POINTER(_Gatt)]

libwarble.warble_gatt_create.restype = POINTER(_Gatt)
libwarble.warble_gatt_create.argtypes = [c_char_p]

libwarble.warble_gatt_create_with_options.restype = POINTER(_Gatt)
libwarble.warble_gatt_create_with_options.argtypes = [c_int, POINTER(_Option)]

libwarble.warble_gatt_find_characteristic.restype = POINTER(_GattChar)
libwarble.warble_gatt_find_characteristic.argtypes = [POINTER(_Gatt), c_char_p]

libwarble.warble_gatt_has_service.restype = c_int
libwarble.warble_gatt_has_service.argtypes = [POINTER(_Gatt), c_char_p]

libwarble.warble_gattchar_disable_notifications_async.restype = None
libwarble.warble_gattchar_disable_notifications_async.argtypes = [POINTER(_GattChar), c_void_p, FnVoid_VoidP_WarbleGattCharP_CharP]

libwarble.warble_gattchar_write_without_resp_async.restype = None
libwarble.warble_gattchar_write_without_resp_async.argtypes = [POINTER(_GattChar), POINTER(c_ubyte), c_ubyte, c_void_p, FnVoid_VoidP_WarbleGattCharP_CharP]

libwarble.warble_gattchar_read_async.restype = None
libwarble.warble_gattchar_read_async.argtypes = [POINTER(_GattChar), c_void_p, FnVoid_VoidP_WarbleGattCharP_UbyteP_Ubyte_CharP]

libwarble.warble_gattchar_write_async.restype = None
libwarble.warble_gattchar_write_async.argtypes = [POINTER(_GattChar), POINTER(c_ubyte), c_ubyte, c_void_p, FnVoid_VoidP_WarbleGattCharP_CharP]

libwarble.warble_gattchar_enable_notifications_async.restype = None
libwarble.warble_gattchar_enable_notifications_async.argtypes = [POINTER(_GattChar), c_void_p, FnVoid_VoidP_WarbleGattCharP_CharP]

libwarble.warble_gattchar_on_notification_received.restype = None
libwarble.warble_gattchar_on_notification_received.argtypes = [POINTER(_GattChar), c_void_p, FnVoid_VoidP_WarbleGattCharP_UbyteP_Ubyte]

libwarble.warble_gattchar_get_uuid.restype = c_char_p
libwarble.warble_gattchar_get_uuid.argtypes = [POINTER(_GattChar)]

libwarble.warble_gattchar_get_gatt.restype = POINTER(_Gatt)
libwarble.warble_gattchar_get_gatt.argtypes = [POINTER(_GattChar)]
