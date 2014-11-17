from . import base
from .types import int

class Packet(base.Packet):
    STATUS_MANUAL_ON = 0x10
    STATUS_MANUAL_OFF = 0x11
    STATUS_STANDBY = 0x15
    STATUS_UNPLUGGED = 0x14
    STATUS_PLUGGED = 0x15
    status = int.IntType(0, 1)
