import sys

class WarbleException(Exception):
    pass

def str_to_bytes(value):
    return value if sys.version_info[0] == 2 else value.encode('utf8')

def bytes_to_str(value):
    return value if sys.version_info[0] == 2 else value.decode('utf8')

from .gatt import *
from .gattchar import *
from .scanner import *
