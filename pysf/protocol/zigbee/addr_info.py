'''Zigbee addr info packet'''
from ...packet import base, fields


class Packet(base.Packet):
    '''Packet class'''
    TYPE_ADDR_JOIN = 0
    TYPE_ADDR_RESOLVE = 1

    type = fields.SizedHex(length=1)
    mac = fields.SizedHex(length=8)
    addr = fields.SizedHex(length=2)
