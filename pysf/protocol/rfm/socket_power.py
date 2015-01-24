'''Socket power'''
from ...packet import base, fields


class Packet(base.Packet):
    '''Power packet structure'''
    voltage = fields.SizedHex(length=2)
    current = fields.SizedHex(length=2)
    power = fields.SizedHex(length=3)
    frequency = fields.SizedHex(length=1)
