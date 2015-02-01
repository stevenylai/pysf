'''Socket status'''
from ...packet import base, fields


class Packet(base.Packet):
    '''Socket status definitions'''
    ON = 0x10
    OFF = 0x11
    STANDBY = 0x15
    UNPLUGGED = 0x14
    PLUGGED = 0x15

    status = fields.SizedHex(length=1)
