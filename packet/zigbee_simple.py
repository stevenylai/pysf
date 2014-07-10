from . import base
from .types import int

class Packet(base.Packet):
    ZB_REQ = 0
    ZB_RES_OK = 1
    ZB_RES_UNKNOWN_CMD = 2
    ZB_RES_TOO_MANY_REQ = 3
    ZB_RES_DEV_NOT_AVAIL = 4
    ZB_RES_DEV_NOT_PAIRED = 5
    ZB_RES_TOO_MANY_PAIRED = 6
    ZB_RES_NETWORK_ERROR = 7
    ZB_RES_INVALID_ADDR = 8
    status = int.IntType(0, 1)
