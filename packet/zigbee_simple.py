from . import base
from .types import int

class Packet(base.Packet):
    ZB_REQ = 0
    ZB_RES_OK = 1
    ZB_RES_UNKNOWN_CMD = 2
    ZB_RES_TOO_MANY_REQ = 3
    ZB_RES_DEV_NOT_AVAIL = 4
    status = int.IntType(0, 1)
