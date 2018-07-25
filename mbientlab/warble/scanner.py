from .cbindings import *
from .cbindings import _Option
from . import WarbleException, str_to_bytes, bytes_to_str
import sys

if sys.version_info[0] == 2:
    range = xrange

class BleScanner:
    @classmethod
    def set_handler(cls, handler):
        """
        Sets a handler to listen for BLE scan results
        @params:
            handler     - Required  : `(ScanResult): void` function that is executed when a device is discovered
        """
        cls.scan_handler = FnVoid_VoidP_WarbleScanResultP(lambda ctx, pointer: handler(ScanResult(pointer.contents)))
        libwarble.warble_scanner_set_handler(None, cls.scan_handler)

    @classmethod
    def start(cls, **kwargs):
        """
        Start BLE scanning
        @params:
            hci         - Optional  : mac address of the hci device to use, only applicable on Linux
            scan_type   - Optional  : type of ble scan to perform, either 'passive' or 'active'
        """
        if (len(kwargs) != 0):
            options = []

            if ('hci' in kwargs and platform.system() == 'Linux'):
                options.append(["hci", kwargs['hci']])
            if ('scan_type' in kwargs):
                options.append(["scan-type", kwargs['scan_type']])
            
            coptions = (_Option * len(options))()
            for i, e in enumerate(options):
                coptions[i] = _Option(key = str_to_bytes(e[0]), value = str_to_bytes(e[1]))

            libwarble.warble_scanner_start(len(options), coptions)
        else:
            libwarble.warble_scanner_start(0, None)

    @classmethod
    def stop(cls):
        """
        Stop BLE scanning
        """
        libwarble.warble_scanner_stop()

class ScanResult:
    def __init__(self, result):
        self.result = result

    @property
    def mac(self):
        """
        Mac address of the scanned device
        """
        return bytes_to_str(self.result.mac)

    @property
    def name(self):
        """
        Device's advertising name
        """
        return bytes_to_str(self.result.name)

    @property
    def rssi(self):
        """
        Device's current signal strength
        """
        return self.result.rssi

    def has_service_uuid(self, uuid):
        """
        True if the device is advertising with the uuid
        @params:
            uuid        - Required  : 128-bit UUID string to search for
        """
        return libwarble.warble_scan_result_has_service_uuid(self.result, str_to_bytes(uuid)) != 0

    def get_manufacturer_data(self, company_id):
        """
        Additional data from the manufacturer included in the scan response, returns `None` if company_id is not found
        @params:
            company_id  - Optional  : Unsigned short value to look up
        """
        pointer = libwarble.warble_scan_result_get_manufacturer_data(self.result, company_id)

        if bool(pointer):
            array = cast(pointer.contents.value, POINTER(c_ubyte * pointer.contents.value_size))
            return [array.contents[i] for i in range(0, pointer.contents.value_size)]
        else:
            return None
